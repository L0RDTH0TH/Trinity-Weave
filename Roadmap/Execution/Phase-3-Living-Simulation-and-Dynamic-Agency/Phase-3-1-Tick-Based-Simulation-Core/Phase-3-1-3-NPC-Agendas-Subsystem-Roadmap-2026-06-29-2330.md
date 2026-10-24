---
title: Phase 3.1.3 — NPC Agendas Subsystem (Execution)
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_living_world_continuity
priority: high
progress: 55
handoff_readiness: 74
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-3
- npc-agendas
- lore-hooks
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roadmap-2026-06-29-2205]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-2-Weather-Environmental-State-Subsystem-Roadmap-2026-06-29-2230]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 3.1.3 — NPC Agendas Subsystem (Execution)

Execution tertiary: second **SimTickPipeline** slot — **AgendaSlotRegistry**, **AvailabilityWindowPolicy**, **LoreHookBindingIndex**, **AgendaProgressState**, **NPCAgendaTickDelta**, **AgendaConflictPolicy**, **OffScreenAgendaDegradePolicy**. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — tone-mood gated availability + lasting progress + off-screen degrade residue **enable** living-world NPC continuity (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Agenda slots + lore hooks → NPCAgendaTickDelta |
| Inspiration / L5 bar (advisory) | Tone-mood gated advance; lasting AgendaProgressState; off-screen degrade residue (never invent narrative); players do not author agendas |
| Inspiration (studied) | (1) Conceptual 3.1.3 + rollup. (2) Execution 3.1 / 3.1.1 / 3.1.2. (3) Phase-2.2 LoreHookRegistry |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + pseudo for availability → hook fire → pick-one conflict → degrade |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 3.1.3 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Sim.Npc.INPCScheduleModule` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_wa_npc_agenda` | `INPCScheduleModule.Tick` / AgendaSlotRegistry | player cannot author slots | AgendaProgressState delta |
| off-screen degrade | `OffScreenAgendaDegradePolicy` | DM pause → no degrade commit | degraded_or_held |
| lore hooks | `LoreHookBindingIndex` | missing binding → Unconfigured | hook arm only |
| faction pressure | consume FactionGraph delta (read) | NPC agenda ≠ faction edge writer | agenda-only TickDelta |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-npc-schedules` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.Npc.INPCScheduleModule` |
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.Npc.INPCScheduleModule` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.Npc.INPCScheduleModule` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `AgendaSlotRegistry` | NPC → agenda slots + priorities |
| `AvailabilityWindowPolicy` | When slots may advance this tick |
| `LoreHookBindingIndex` | Slot → lore hook ids (Phase-2.2) |
| `AgendaProgressState` | Per-NPC progress / cooldown |
| `AgendaConflictPolicy` | Pick-one when multiple slots fire |
| `OffScreenAgendaDegradePolicy` | Background degrade while off-camera |
| `NPCAgendaTickDelta` | Per-tick output payload |
| `NPCAgendaSubsystem` | ISimSubsystem adapter (`slot_id: npc_agendas`) |

## Interfaces

```text
NPCAgendaTickDelta (RefCounted):
  + tick_id: int
  + npc_deltas: Dictionary   # npc_id -> {slot_id, progress, hooks_fired, side_effects}
  + overflow: bool
  + deferred_npcs: PackedStringArray
  + to_dict() -> Dictionary

AgendaSlot (RefCounted):
  + slot_id: StringName
  + npc_id: StringName
  + priority: int
  + hook_ids: PackedStringArray
  + enabled: bool
  + to_dict() -> Dictionary

AgendaSlotRegistry (RefCounted):
  + slots_for(npc_id: StringName) -> Array
  + register(slot: AgendaSlot) -> Error
  + seed_from(sim_graph: Dictionary) -> Error
  signals: slot_changed(npc_id, slot_id)

AvailabilityWindowPolicy (RefCounted):
  + is_available(slot: AgendaSlot, sim_time: float, mood: Dictionary) -> bool

LoreHookBindingIndex (RefCounted):
  + hooks_for(slot_id: StringName) -> PackedStringArray
  + bind(slot_id: StringName, hook_ids: PackedStringArray) -> Error

AgendaProgressState (RefCounted):
  + get_progress(npc_id: StringName, slot_id: StringName) -> float
  + advance(npc_id: StringName, slot_id: StringName, amount: float) -> void
  + cooldown_ok(npc_id: StringName, slot_id: StringName, sim_time: float) -> bool

AgendaConflictPolicy (RefCounted):
  + pick_one(candidates: Array) -> AgendaSlot
  # stable: highest priority, then slot_id lexicographic

OffScreenAgendaDegradePolicy (RefCounted):
  + degrade(npc_id: StringName, dt: float, off_screen: bool) -> Dictionary
  # returns {progress_delta, deferred_to_3_2:bool}

NPCAgendaSubsystem (RefCounted):  # ISimSubsystem
  + slot_id() -> StringName  # &"npc_agendas"
  + tick(sim_time: float, snapshot: Dictionary) -> Dictionary
  signals: agenda_tick_ready(delta)
```

## Pseudo-code

```pseudo
# 3.1.3 — NPCAgendaSubsystem second SimTickPipeline slot (Godot 4 stable).
# Citations: RefCounted, PackedStringArray, Error/OK.
#
# === JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# Tone-weighted: AvailabilityWindowPolicy uses weather_mood (from 3.1.2 ToneProfile path).
# Lasting world: AgendaProgressState.advance persists — durable readable progress.
# Off-screen residue: OffScreenAgendaDegradePolicy — NEVER invent on-screen narrative; defer to 3.2.
# Budget residue: overflow → deferred_npcs — NEVER silent truncate.
# Players do not author agendas; lore hooks MUST exist in Phase-2.2 — no invented facts.
# ===========================================================

class_name NPCAgendaSubsystem
extends RefCounted

signal agenda_tick_ready(delta)

var _registry: AgendaSlotRegistry
var _availability: AvailabilityWindowPolicy
var _hooks: LoreHookBindingIndex
var _progress: AgendaProgressState
var _conflict: AgendaConflictPolicy
var _degrade: OffScreenAgendaDegradePolicy
var _scheduler_budget_ms: float = 6.0

func slot_id() -> StringName:
	return &"npc_agendas"

func tick(sim_time: float, snapshot: Dictionary) -> Dictionary:
	var mood: Dictionary = snapshot.get("weather_mood", {})  # tone-weighted from 3.1.2
	var npc_ids: Array = snapshot.get("active_npc_ids", [])
	var out := NPCAgendaTickDelta.new()
	out.tick_id = int(snapshot.get("tick_id", 0))
	out.npc_deltas = {}
	out.overflow = false
	out.deferred_npcs = PackedStringArray()
	var t0 := Time.get_ticks_msec()
	for npc_id in npc_ids:
		if float(Time.get_ticks_msec() - t0) > _scheduler_budget_ms:
			# JUNIOR WORK-ORDER: budget residue — defer, never truncate
			out.overflow = true
			out.deferred_npcs.append(str(npc_id))
			continue
		var off_screen: bool = bool(snapshot.get("off_screen", {}).get(npc_id, false))
		if off_screen:
			# JUNIOR WORK-ORDER: off-screen residue — degrade only, never invent narrative
			var deg := _degrade.degrade(npc_id, snapshot.get("dt", 0.0), true)
			out.npc_deltas[npc_id] = {"degrade": deg, "off_screen": true}
			continue
		var candidates: Array = []
		for slot in _registry.slots_for(npc_id):
			if not slot.enabled:
				continue
			# JUNIOR WORK-ORDER: tone-mood gate (living world continuity)
			if not _availability.is_available(slot, sim_time, mood):
				continue
			if not _progress.cooldown_ok(npc_id, slot.slot_id, sim_time):
				continue
			candidates.append(slot)
		if candidates.is_empty():
			continue
		var chosen: AgendaSlot = _conflict.pick_one(candidates)
		var fired := _hooks.hooks_for(chosen.slot_id)
		# JUNIOR WORK-ORDER: lasting world — progress advance required
		_progress.advance(npc_id, chosen.slot_id, 1.0)
		out.npc_deltas[npc_id] = {
			"slot_id": chosen.slot_id,
			"hooks_fired": fired,
			"side_effects": {"faction_hints": true},
		}
	agenda_tick_ready.emit(out)
	var d := out.to_dict()
	d["overflow"] = out.overflow
	return d

# Lore hooks via Phase-2.2 — agendas never invent facts. Packaging → 3.2.

# === WEAVE C# / .NET (Godot 4.6.3) — ISimTickHost ===
# Manifest: stack-npc-schedules, stack-simulation-tick, engine-godot-463-dotnet | Catalog: ux_living_world_continuity
namespace Genesis.Sim;

public interface ISimTickHost {
    Error Tick(double simTime, SimSnapshot snapshot);
}

public sealed partial class SimTickHost : Node, ISimTickHost {
    // JUNIOR WORK-ORDER (ux_living_world_continuity): lasting residue; overflow deferred not dropped
    // ACCEPT: modules tick in order; VERIFY no Autoload god-object
    public Error Tick(double simTime, SimSnapshot snapshot) {
        foreach (var mod in _modules) mod.Tick(simTime, snapshot.ToDict());
        return Error.Ok;
    }
}

```

## Invariants

| ID | Rule |
|----|------|
| I-3.1.3-001 | Slot order: npc_agendas after weather, before faction_graph |
| I-3.1.3-002 | At most one agenda slot advances per NPC per tick (pick-one) |
| I-3.1.3-003 | Lore hooks must exist in Phase-2.2 index — no invented hook ids |
| I-3.1.3-004 | Off-screen degrade never fabricates on-screen narrative events |
| I-3.1.3-005 | Budget overflow sets `overflow:true` + deferred_npcs |
| I-3.1.3-006 | **L5:** tone-mood gate + lasting progress + off-screen residue preserve living world |

## Acceptance

- [x] Parallel spine under Phase-3-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 3.1.3
- [x] Module map + interfaces + pseudo for NPCAgendaSubsystem
- [x] **UX Catalog paint** — L5 tone/lasting/residue as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `INPCScheduleModule` tick/admit path fails closed (Unauthorized|InvalidParameter|Busy) on wrong seat / null input — row `ux_living_world_continuity`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player seat, **When** AgendaSlotRegistry write, **Then** Unauthorized and AgendaProgressState unchanged
- [ ] **Given** NPCAgendaTickDelta commit, **When** keys include faction edge mutations, **Then** InvalidParameter — agenda delta is agenda-only
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Research integration

- No Autoload NPC AI; RefCounted subsystem behind Simulation pipeline.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Next paint cursor: **3.1.4** FactionGraph (this wave).

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **3.1.4**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
