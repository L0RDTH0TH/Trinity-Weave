---
title: Phase 3.1.4 — FactionGraph Subsystem (Execution)
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.4"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-4-FactionGraph-Subsystem-Roadmap-2026-06-30-0015]]'
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
- faction-graph
- reputation
- tension
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-4-FactionGraph-Subsystem-Roadmap-2026-06-30-0015]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-2-Weather-Environmental-State-Subsystem-Roadmap-2026-06-29-2230]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 3.1.4 — FactionGraph Subsystem (Execution)

Execution tertiary: third **SimTickPipeline** slot — **FactionGraphRegistry**, **EdgeWeightPolicy**, **ThresholdRuleIndex**, **OffScreenEventScheduler**, **GraphConflictPolicy**, **TribeMembershipIndex**, **FactionGraphTickDelta**. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — lasting edge patches + tone-mood thresholds + off-screen math arms **enable** living-world faction continuity; narrative packaging stays in **3.2**.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Edges + thresholds → FactionGraphTickDelta |
| Inspiration / L5 bar (advisory) | Lasting edge apply_patch; tone-mood threshold eval; off-screen math residue (no narrative invent); players do not author graph |
| Inspiration (studied) | (1) Conceptual 3.1.4 + rollup. (2) Execution 3.1 / 3.1.3. (3) Phase-2.1 SimGraphSeed |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + pseudo for decay → threshold → off-screen arm → pick-one |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 3.1.4 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Sim.Faction.FactionGraph` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_wa_faction_offscreen` | FactionGraph edge update | player cannot author faction | off-screen edge + cost |
| `ux_wa_npc_agenda` | NPC agendas consume faction pressure | observe-only refuse write | agenda delta |
| canon conflict | ConsequenceResolver precedence | canon > faction | reject invent |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.Faction.FactionGraph` |
| `stack-intent-lore-loop` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.Faction.FactionGraph` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.Faction.FactionGraph` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `FactionGraphRegistry` | Nodes {faction_id, tribe_id} + edges {src, dst, edge_kind, weight} |
| `EdgeWeightPolicy` | decay_rate / min / max per edge_kind |
| `ThresholdRuleIndex` | rule_id → predicate + edge_mutation + cooldown |
| `OffScreenEventScheduler` | Background-region event arms (math only) |
| `GraphConflictPolicy` | One committing mutation per (src, dst, edge_kind) per tick |
| `TribeMembershipIndex` | tribe_id → parent_faction_id |
| `FactionGraphTickDelta` | Graph-scoped patches only — never NPC agenda keys |
| `FactionGraphSubsystem` | ISimSubsystem adapter (`slot_id: faction_graph`) |

## Interfaces

```text
FactionGraphTickDelta (RefCounted):
  + tick_id: int
  + edge_patches: Array   # [{src, dst, edge_kind, weight_delta, rule_id}]
  + membership_stale: bool
  + overflow: bool
  + deferred_regions: PackedStringArray
  + to_dict() -> Dictionary

FactionEdge (RefCounted):
  + src: StringName
  + dst: StringName
  + edge_kind: StringName   # reputation | tension | treaty | trade
  + weight: float
  + to_dict() -> Dictionary

FactionGraphRegistry (RefCounted):
  + edges_in(region_id: StringName) -> Array
  + apply_patch(patch: Dictionary) -> Error
  + seed_from(sim_graph: Dictionary) -> Error
  signals: edge_changed(src, dst, edge_kind)

EdgeWeightPolicy (RefCounted):
  + passive_decay(edges: Array, dt: float) -> Array
  + clamp_weight(edge_kind: StringName, weight: float) -> float

ThresholdRuleIndex (RefCounted):
  + evaluate(decayed: Array, npc_side_effects_ro: Dictionary, mood: Dictionary) -> Array
  # returns candidate mutations; RO on 3.1.3 side_effects

OffScreenEventScheduler (RefCounted):
  + advance(region_id: StringName, sim_time: float) -> Array
  # math arms only — no narrative strings

GraphConflictPolicy (RefCounted):
  + pick_one_per_edge_key(candidates: Array) -> Array
  # stable: highest rule priority, then rule_id lexicographic

TribeMembershipIndex (RefCounted):
  + parent_faction(tribe_id: StringName) -> StringName
  + is_stale(snapshot_gen: int) -> bool

FactionGraphSubsystem (RefCounted):  # ISimSubsystem
  + slot_id() -> StringName  # &"faction_graph"
  + tick(sim_time: float, snapshot: Dictionary) -> Dictionary
  signals: faction_tick_ready(delta)
```

## Pseudo-code

```pseudo
# 3.1.4 — FactionGraphSubsystem third SimTickPipeline slot (Godot 4 stable).
# Citations: RefCounted, PackedStringArray, Error/OK, StringName.
#
# === JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# Tone-weighted: ThresholdRuleIndex.evaluate MUST pass weather_mood (ToneProfile path).
# Lasting world: apply_patch on chosen mutations — durable edge state.
# Off-screen residue: OffScreenEventScheduler.advance = math arms ONLY — NEVER invent narrative (3.2 packs).
# Budget residue: overflow → deferred_regions — NEVER silent truncate.
# Players do not author graph; never write NPC agenda keys into FactionGraphTickDelta.
# ===========================================================

class_name FactionGraphSubsystem
extends RefCounted

signal faction_tick_ready(delta)

var _registry: FactionGraphRegistry
var _decay: EdgeWeightPolicy
var _thresholds: ThresholdRuleIndex
var _offscreen: OffScreenEventScheduler
var _conflict: GraphConflictPolicy
var _membership: TribeMembershipIndex
var _scheduler_budget_ms: float = 6.0

func slot_id() -> StringName:
	return &"faction_graph"

func tick(sim_time: float, snapshot: Dictionary) -> Dictionary:
	var out := FactionGraphTickDelta.new()
	out.tick_id = int(snapshot.get("tick_id", 0))
	out.edge_patches = []
	out.membership_stale = false
	out.overflow = false
	out.deferred_regions = PackedStringArray()
	if _membership.is_stale(int(snapshot.get("membership_gen", 0))):
		out.membership_stale = true
		faction_tick_ready.emit(out)
		return out.to_dict()
	var mood: Dictionary = snapshot.get("weather_mood", {})  # tone-weighted
	var npc_fx: Dictionary = snapshot.get("npc_agenda_side_effects", {})
	var regions: Array = snapshot.get("active_region_ids", [])
	var t0 := Time.get_ticks_msec()
	var candidates: Array = []
	for region_id in regions:
		if float(Time.get_ticks_msec() - t0) > _scheduler_budget_ms:
			# JUNIOR WORK-ORDER: budget residue — defer, never truncate
			out.overflow = true
			out.deferred_regions.append(str(region_id))
			continue
		var edges: Array = _registry.edges_in(region_id)
		var decayed: Array = _decay.passive_decay(edges, float(snapshot.get("dt", 0.0)))
		# JUNIOR WORK-ORDER: tone-mood thresholds (living world continuity)
		candidates.append_array(_thresholds.evaluate(decayed, npc_fx, mood))
		if bool(snapshot.get("background_regions", {}).get(region_id, false)):
			# JUNIOR WORK-ORDER: off-screen math arms only — no narrative invent
			candidates.append_array(_offscreen.advance(region_id, sim_time))
	var chosen: Array = _conflict.pick_one_per_edge_key(candidates)
	for patch in chosen:
		# JUNIOR WORK-ORDER: lasting world — apply_patch required
		var err := _registry.apply_patch(patch)
		if err == OK:
			out.edge_patches.append(patch)
	faction_tick_ready.emit(out)
	var d := out.to_dict()
	d["overflow"] = out.overflow
	return d

# Narrative packaging / SinceYouLeft → Phase 3.2. Merge above NPC/weather, below canon.

# === WEAVE C# / .NET (Godot 4.6.3) — ISimTickHost ===
# Manifest: stack-simulation-tick, stack-intent-lore-loop, engine-godot-463-dotnet | Catalog: ux_living_world_continuity
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
| I-3.1.4-001 | Slot order: faction_graph after npc_agendas; before ConsequenceResolver |
| I-3.1.4-002 | At most one mutation per (src, dst, edge_kind) per tick |
| I-3.1.4-003 | FactionGraphTickDelta never carries NPC agenda progress keys |
| I-3.1.4-004 | OffScreenEventScheduler arms math only — no narrative compile |
| I-3.1.4-005 | Stale TribeMembershipIndex → membership_stale; block dependent commits |
| I-3.1.4-006 | **L5:** tone thresholds + lasting patches + off-screen math preserve living world |

## Acceptance

- [x] Parallel spine under Phase-3-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 3.1.4
- [x] Module map + interfaces + pseudo for FactionGraphSubsystem
- [x] **UX Catalog paint** — L5 tone/lasting/residue as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `FactionGraph` tick/admit path fails closed (Unauthorized|InvalidParameter|Busy) on wrong seat / null input — row `ux_living_world_continuity`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player seat, **When** FactionGraph edge update, **Then** Unauthorized and no edge mutation lands
- [ ] **Given** dual committing mutations same (src,dst,edge_kind) one tick, **When** GraphConflictPolicy applies, **Then** one winner + reject invent — never silent double write
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Research integration

- Simulation-layer RefCounted subsystem; no GraphEdit as authority.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Next paint cursor: **3.2** Off-Screen Activity (this wave).

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **3.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
