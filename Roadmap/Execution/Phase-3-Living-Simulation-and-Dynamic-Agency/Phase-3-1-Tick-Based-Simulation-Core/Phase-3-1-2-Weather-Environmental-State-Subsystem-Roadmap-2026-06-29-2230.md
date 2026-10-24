---
title: Phase 3.1.2 — Weather Environmental State Subsystem (Execution)
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-2-Weather-Environmental-State-Subsystem-Roadmap-2026-06-29-2230]]'
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
- weather
- environmental-state
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-2-Weather-Environmental-State-Subsystem-Roadmap-2026-06-29-2230]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roadmap-2026-06-29-2205]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 3.1.2 — Weather Environmental State Subsystem (Execution)

Execution tertiary: first **SimTickPipeline** slot — **RegionWeatherRegistry**, **EnvironmentalCycleProfile**, **MoodModifierBinding**, **WeatherTickDelta**, **RegionScopeResolver**, **WeatherNoisePolicy**. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — ToneProfile-weighted weather/mood + lasting registry upserts **enable** living-world continuity (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Region weather + mood deltas → ConsequenceResolver (low precedence) |
| Inspiration / L5 bar (advisory) | Tone-aware weather shape; lasting RegionWeatherRegistry; overflow residue deferred not truncated; players do not author weather |
| Inspiration (studied) | (1) Conceptual 3.1.2 + rollup. (2) Execution 3.1 pipeline slot. (3) 3.1.1 clock. (4) Phase-2.3 tone |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + pseudo for scope → cycle → noise clamp → WeatherTickDelta |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 3.1.2 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Sim.Weather.IWeatherModule` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_sim_weather_pulse` | `IWeatherModule.Tick` / `WeatherEnvState` | budget overflow → deferred_regions | RegionWeatherRegistry upsert |
| ToneProfile mood weight | ToneProfileConsequenceWeights → weather slot | missing profile → Unconfigured | felt weather delta |
| lasting readable costs | Registry upsert + WorldEventLog | Presentation VFX must not write registry | lasting weather row |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-weather-ambience` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.Weather.IWeatherModule` |
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.Weather.IWeatherModule` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.Weather.IWeatherModule` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `RegionWeatherRegistry` | Region_id → weather keys + intensity |
| `EnvironmentalCycleProfile` | Diurnal / seasonal cycle curves |
| `MoodModifierBinding` | Weather → mood delta bindings (tone-aware) |
| `RegionScopeResolver` | Which regions tick this frame (budget-aware) |
| `WeatherNoisePolicy` | Clamp / seed-stable noise for drift |
| `WeatherTickDelta` | Per-tick output payload |
| `WeatherEnvState` | ISimSubsystem adapter (`slot_id: weather`) |

## Interfaces

```text
WeatherTickDelta (RefCounted):
  + tick_id: int
  + region_deltas: Dictionary   # region_id -> {weather_key, intensity, mood_delta}
  + overflow: bool
  + deferred_regions: PackedStringArray
  + to_dict() -> Dictionary

RegionWeatherEntry (RefCounted):
  + region_id: StringName
  + weather_key: StringName
  + intensity: float
  + mood_bias: float
  + to_dict() -> Dictionary

RegionWeatherRegistry (RefCounted):
  + get_entry(region_id: StringName) -> RegionWeatherEntry
  + upsert(entry: RegionWeatherEntry) -> Error
  + seed_from(sim_graph: Dictionary) -> Error
  signals: weather_entry_changed(region_id)

EnvironmentalCycleProfile (RefCounted):
  + sample(sim_time: float, region_id: StringName) -> Dictionary
  # { weather_key, base_intensity }

MoodModifierBinding (RefCounted):
  + mood_delta(weather_key: StringName, intensity: float, tone: Dictionary) -> float

RegionScopeResolver (RefCounted):
  + regions_for_tick(snapshot: Dictionary, budget_remaining_ms: float) -> PackedStringArray
  signals: scope_truncated(count)

WeatherNoisePolicy (RefCounted):
  + apply(base: Dictionary, map_seed: int, tick_id: int) -> Dictionary
  # seed-stable; clamps intensity to [0,1]

WeatherEnvState (RefCounted):  # ISimSubsystem
  + slot_id() -> StringName  # &"weather"
  + tick(sim_time: float, snapshot: Dictionary) -> Dictionary
  signals: weather_tick_ready(delta)
```

## Pseudo-code

```pseudo
# 3.1.2 — WeatherEnvState first SimTickPipeline slot (Godot 4 stable).
# Citations: RefCounted, PackedStringArray, Error/OK.
#
# === JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# Tone-weighted living world: MoodModifierBinding.mood_delta MUST pass Phase-2 ToneProfile (_tone).
# Lasting world: every region tick MUST RegionWeatherRegistry.upsert — durable readable state.
# Off-screen residue: budget overflow → deferred_regions + overflow:true — NEVER silent truncate.
# Players do not author weather — Presentation mirrors RO; never writes registry.
# Weather never invents/overrides canon (ConsequenceResolver: weather LAST).
# ===========================================================

class_name WeatherEnvState
extends RefCounted

signal weather_tick_ready(delta)

var _registry: RegionWeatherRegistry
var _cycle: EnvironmentalCycleProfile
var _mood: MoodModifierBinding
var _scope: RegionScopeResolver
var _noise: WeatherNoisePolicy
var _tone: Dictionary = {}       # Phase-2 ToneProfileConsequenceWeights
var _map_seed: int = 0
var _scheduler_budget_ms: float = 4.0

func slot_id() -> StringName:
	return &"weather"

func tick(sim_time: float, snapshot: Dictionary) -> Dictionary:
	var regions := _scope.regions_for_tick(snapshot, _scheduler_budget_ms)
	var out := WeatherTickDelta.new()
	out.tick_id = int(snapshot.get("tick_id", 0))
	out.region_deltas = {}
	out.overflow = false
	out.deferred_regions = PackedStringArray()
	var t0 := Time.get_ticks_msec()
	for rid in regions:
		if float(Time.get_ticks_msec() - t0) > _scheduler_budget_ms:
			# JUNIOR WORK-ORDER: off-screen / budget residue — defer, never truncate
			out.overflow = true
			out.deferred_regions.append(rid)
			continue
		var base := _cycle.sample(sim_time, rid)
		var noised := _noise.apply(base, _map_seed, out.tick_id)
		var intensity: float = float(noised.get("intensity", 0.0))
		# JUNIOR WORK-ORDER: tone-weighted weather → mood (living world continuity)
		var mood := _mood.mood_delta(noised.get("weather_key", &""), intensity, _tone)
		var entry := RegionWeatherEntry.new()
		entry.region_id = rid
		entry.weather_key = noised.get("weather_key", &"clear")
		entry.intensity = intensity
		entry.mood_bias = mood
		# JUNIOR WORK-ORDER: lasting world state — registry required
		_registry.upsert(entry)
		out.region_deltas[rid] = entry.to_dict()
	weather_tick_ready.emit(out)
	var d := out.to_dict()
	d["overflow"] = out.overflow
	return d

# Merge precedence: canon > faction > NPC > weather. Seed via registry.seed_from.

# === WEAVE C# / .NET (Godot 4.6.3) — replaces GDScript-first theater ===
# Manifest: stack-weather-ambience, stack-simulation-tick, engine-godot-463-dotnet | Catalog: ux_living_world_continuity

namespace Genesis.Sim.Weather;

public interface IWeatherModule {
    StringName SlotId { get; }
    WeatherTickDelta Tick(double simTime, Godot.Collections.Dictionary snapshot);
}

public sealed partial class WeatherEnvState : RefCounted, IWeatherModule {
    // JUNIOR WORK-ORDER (ux_living_world_continuity): ux_sim_weather_pulse — felt weather, lasting registry
    // ACCEPT: Given ToneProfile, When Tick under budget, Then Upsert + deferred_regions if overflow
    // VERIFY: Presentation never writes RegionWeatherRegistry; gdUnit4Net overflow case
    public StringName SlotId => new StringName("weather");
    public required RegionWeatherRegistry Registry { get; init; }
    public WeatherTickDelta Tick(double simTime, Godot.Collections.Dictionary snapshot) {
        if (snapshot == null) throw new System.ArgumentNullException(nameof(snapshot));
        // Graybox OK: compute ≥1 region delta OR set Overflow+deferred_regions — never silent empty theater
        // Full algorithm: Phase-3.1.2 leaf; contracts: [[Docs/SeamRegistry-CSharp-Host-Index]] §B2
        var delta = new WeatherTickDelta { RegionCount = 1 };
        if (IsOverBudget(delta)) { delta.Overflow = true; delta.DeferredRegions = ListDeferred(snapshot); }
        Registry.Upsert(delta);
        return delta;
    }
}

```

## Invariants

| ID | Rule |
|----|------|
| I-3.1.2-001 | Slot order: weather is first subsystem in SimTickPipeline |
| I-3.1.2-002 | Budget overflow sets `overflow:true` + lists deferred regions |
| I-3.1.2-003 | Noise is map_seed + tick_id stable — no wall-clock entropy |
| I-3.1.2-004 | Weather cannot invent or override canon facts |
| I-3.1.2-005 | Presentation VFX may mirror deltas — never write registry |
| I-3.1.2-006 | **L5:** ToneProfile mood + lasting upsert preserve living-world continuity |

## Acceptance

- [x] Parallel spine under Phase-3-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 3.1.2
- [x] Module map + interfaces + pseudo for WeatherEnvState
- [x] **UX Catalog paint** — L5 tone-weighted weather / lasting / residue as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `IWeatherModule` tick/admit path fails closed (Unauthorized|InvalidParameter|Busy) on wrong seat / null input — row `ux_living_world_continuity`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** Tick budget overflow on IWeatherModule.Tick, **When** commit, **Then** Overflow/deferred_regions set and RegionWeatherRegistry is not silently truncated
- [ ] **Given** Presentation VFX path, **When** registry write attempted, **Then** Unauthorized — lasting weather row only from module upsert
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Research integration

- No Autoload weather service; lives as RefCounted behind Simulation pipeline.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Next paint cursor: **3.1.3** NPC Agendas (this wave).

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **3.1.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
