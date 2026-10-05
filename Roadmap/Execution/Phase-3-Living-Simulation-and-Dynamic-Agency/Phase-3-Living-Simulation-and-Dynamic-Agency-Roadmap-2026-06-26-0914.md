---
title: Phase 3 — Living Simulation and Dynamic Agency (Execution)
roadmap-level: primary
phase-number: 3
subphase-index: "3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_living_world_continuity
priority: high
progress: 85
handoff_readiness: 68
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-28
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-3
- living-simulation
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-2-Off-Screen-Faction-Tribe-Activity/Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
stack_weave_decollapse: true
---
# Phase 3 — Living Simulation and Dynamic Agency (Execution)

Execution primary: tick spine, off-screen deltas, DM overwrite vs re-gen policy. Parallel spine under `Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/`. **No Half B.** L5/SERIES are **read-only advisory feedstock** — lasting world continuity + tone-weighted sim + off-screen residue **enable** persistent living world (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Persistent balanced simulation with DM authority respected |
| Inspiration / L5 bar (advisory) | Durable lasting world state; tone-aware weather/NPC; off-screen residues; every world-hitting change DM-retconnable |
| Inspiration (studied) | (1) Conceptual Phase 3 + secondaries 3.1–3.3. (2) Execution Phase-2 SimGraphSeed / WorldEventLogInitializer. (3) WorldShell disposable container research |
| Execution mechanism | Module map + interfaces for SimClock / tick pipeline / off-screen compiler / overwrite patch layer |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual Phase 3 + 3.1–3.3 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Sim.ISimTickHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_sim_weather_pulse` | `WeatherEnvState` via `ISimTickHost.Tick` | weather owns pulse; clock ≠ writer | RegionWeatherRegistry upsert |
| `ux_wa_faction_offscreen` | `FactionGraphSubsystem` slot | player seat cannot author edges | lasting edge + cost patch |
| `ux_wa_npc_agenda` | `NPCAgendaSubsystem` slot | observe-only refuse agenda write | agenda progress delta |
| `ux_canon_pipeline_feel` | `ConsequenceResolver` + WorldEventLog | canon > faction/agenda invent | committed event row |

## Tech stack weave

**De-collapse rule:** weather / NPC / faction / engine rows **must not** all point at `ISimTickHost`. Tick host orchestrates; leaf ports own their stack ids. Signatures: [[Docs/SeamRegistry-CSharp-Host-Index]] §B2.

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-simulation-tick` | `ISimTickHost` + TickScheduler | `Genesis.Sim.ISimTickHost` — orchestrates ordered slots only |
| `stack-weather-ambience` | `IWeatherModule` | `Genesis.Sim.IWeatherModule` (3.1.2) — **not** tick host |
| `stack-npc-schedules` | `INPCScheduleModule` | `Genesis.Sim.INPCScheduleModule` (3.1.3) — **not** tick host |
| `stack-faction-graph` | FactionGraph port | `Genesis.Sim.IFactionGraph` (3.1.4) — off-screen edges; **not** tick host |
| `engine-godot-463-dotnet` | Godot 4.6.3 .NET / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` — **not** a sim port |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net ≥1 happy + ≥1 refuse per host |

## Module map

| Module | Responsibility | Owner secondary |
|--------|----------------|-----------------|
| `SimClock` | Authoritative sim time + pause | 3.1 / 3.1.1 |
| `TickScheduler` | Ordered subsystem dispatch caps | 3.1 / 3.1.1 |
| `SimTickPipeline` | Weather → NPC → FactionGraph tick | 3.1 |
| `WorldEventLog` | Append-only committed tick records | 3.1 (from Phase-2 initializer) |
| `WeatherEnvState` | Environmental state channel | 3.1.2 |
| `NPCAgendaSubsystem` | Off-camera NPC agendas | 3.1.3 |
| `FactionGraphSubsystem` | Faction edge updates | 3.1.4 |
| `OffScreenActivityWindow` | Capture window since player left | 3.2 |
| `SinceYouLeftCompiler` | NarrativeDelta from off-screen | 3.2 |
| `DMOverwriteClass` | Classify DM patches vs regen | 3.3 |
| `OverwritePatchLayer` | Apply DM patches without full regen | 3.3 |
| `ReGenerationIntentQueue` | Queued deliberate re-gen intents | 3.3 |
| `DMPauseGate` | Queue speculative deltas while DM paused | 3.3 |

## Interfaces

```text
CommittedTickRecord (RefCounted):
  + tick_id: int
  + sim_time: float
  + subsystem_deltas: Dictionary
  + provenance: Dictionary
  + to_dict() -> Dictionary

NarrativeDelta (RefCounted):
  + delta_id: StringName
  + severity: int
  + faction_ids: PackedStringArray
  + summary_key: StringName
  + route: StringName   # auto_brief | dm_queue | suppress
  + provenance: Dictionary
  + to_dict() -> Dictionary

ReGenerationIntent (RefCounted):
  + intent_id: StringName
  + scope: Dictionary
  + reason: StringName
  + dm_actor: StringName
  + to_dict() -> Dictionary

SimClock (RefCounted):
  + now() -> float
  + pause() -> void
  + resume() -> void
  + advance(dt: float) -> Error
  signals: tick_started(tick_id), tick_advanced(tick_id, sim_time), sim_paused(), sim_resumed()

SimTickPipeline (Node under Simulation layer — NOT Autoload world root):
  + run_tick() -> Error
  + last_record() -> CommittedTickRecord
  signals: tick_complete(record), tick_aborted(reason)

OffScreenActivityWindow (RefCounted):
  + span(session: Dictionary) -> Dictionary  # {tick_depart, tick_return, wall_dt}
  + mark_presence(tick_id: int) -> void
  signals: window_opened(), window_closed(delta_id)

DMPauseGate (RefCounted):
  + is_paused() -> bool
  + may_advance() -> bool   # false while paused; 3.1.1 ClockBridge may wrap
  + pause(reason: StringName) -> void
  + resume() -> void
  + queue_speculative(delta: Dictionary) -> void
  signals: sim_paused(reason), sim_resumed()

DMOverwriteClass / OverwritePatchLayer (RefCounted):
  + classify(patch: Dictionary) -> StringName
  + apply(patch: Dictionary) -> Error
  signals: overwrite_applied(patch_id), re_gen_queued(intent_id)
```

## Pseudo-code

```pseudo
# Phase 3 primary — Living simulation spine (Godot 4 stable).
# Citations: Node children under Simulation layer; Error/OK; queue_free on regen swap.
#
# === JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# Lasting world: every successful tick MUST WorldEventLog.append — durable readable state.
# Tone-weighted living world: weather/NPC/faction tick under ToneProfileConsequenceWeights (Phase-2).
# Off-screen residue: overflow → TickScheduler defer — NEVER silent truncate (SinceYouLeft later).
# DM-retconnable: DMPauseGate pause → queue_speculative — never invent facts mid-pause.
# Players do not author ticks — Presentation consumes tick_complete async only.
# ===========================================================

class_name SimTickPipeline
extends Node

signal tick_complete(record)
signal tick_aborted(reason)

var _clock: SimClock
var _weather: RefCounted      # WeatherEnvState — 3.1.2 (tone-weighted)
var _npc: RefCounted          # NPCAgendaSubsystem — 3.1.3 (tone-weighted)
var _factions: RefCounted     # FactionGraphSubsystem — 3.1.4
var _log: RefCounted          # WorldEventLog — lasting world residue
var _pause_gate: RefCounted   # DMPauseGate — 3.3
var _tick_id: int = 0

func run_tick() -> Error:
	# JUNIOR WORK-ORDER: DM pause = retconnable hold — queue, do not invent
	if _pause_gate != null and _pause_gate.is_paused():
		_pause_gate.queue_speculative({"tick": _tick_id + 1})
		return ERR_BUSY
	_tick_id += 1
	_clock.tick_started.emit(_tick_id)
	var deltas := {}
	for sub in [_weather, _npc, _factions]:
		if sub == null:
			continue
		var d: Dictionary = sub.tick(_clock.now(), snapshot)
		if d.get("overflow", false):
			# JUNIOR WORK-ORDER: off-screen / budget overflow → defer, never truncate
			deltas[sub.get_class()] = d
			continue
		deltas[sub.get_class()] = d
	var rec := CommittedTickRecord.new()
	rec.tick_id = _tick_id
	rec.sim_time = _clock.now()
	rec.subsystem_deltas = deltas
	# JUNIOR WORK-ORDER: lasting world state — log required for durable living world
	var err := _log.append(rec)
	if err != OK:
		tick_aborted.emit("log_append")
		return err
	tick_complete.emit(rec)  # Presentation async only
	return OK

# Ordering: 3.1 tick spine BEFORE 3.2 SinceYouLeftCompiler surfacing.
# 3.3 reconciler runs on DMPauseGate resume — never invents facts mid-pause.
# SimGraphSeed from Phase 2.1 seeds initial FactionGraph / NPC agendas.

# === WEAVE C# / .NET (Godot 4.6.3) — ISimTickHost ===
# Manifest: stack-simulation-tick, stack-weather-ambience, stack-npc-schedules, engine-godot-463-dotnet | Catalog: ux_living_world_continuity
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
| I-3-001 | Tick spine (3.1) precedes off-screen narrative compile (3.2) |
| I-3-002 | DMPauseGate speculative deltas reconcile only via 3.3 — no silent drop |
| I-3-003 | Deliberate re-gen goes through ReGenerationIntentQueue + Phase-2 DryRun path |
| I-3-004 | SimTickPipeline lives under Simulation layer Node — not Autoload world root |
| I-3-005 | Off-screen overflow defers per TickScheduler caps — not truncated silently |
| I-3-006 | **L5:** WorldEventLog append + tone weights preserve lasting living-world continuity |

## Acceptance

- [x] Parallel spine path `Execution/Phase-3-…/` (primary)
- [x] Path-qualified `conceptual_counterpart` → frozen Phase 3
- [x] Module map + child index for 3.1 / 3.2 / 3.3
- [x] Interfaces + primary pseudo for SimTickPipeline / clock / overwrite hooks
- [x] Secondary **3.1** Tick-Based Simulation Core minted
- [x] Tertiaries **3.1.1 / 3.1.2 / 3.1.3** minted (DFS wave)
- [x] Tertiary **3.1.4** FactionGraph minted
- [x] Secondary **3.2** Off-Screen Activity minted
- [x] Secondary **3.3** DM Overwrite / Re-Gen minted
- [x] **UX Catalog paint** — L5 living-world continuity as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `ISimTickHost` tick/admit path fails closed (Unauthorized|InvalidParameter|Busy) on wrong seat / null input — row `ux_living_world_continuity`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** Tick with weather+faction+NPC slots, **When** pipeline commits, **Then** each slot writes its own TickDelta (weather≠faction≠agenda) and WorldEventLog gains lasting cost rows — never one universal residue blob
- [ ] **Given** player seat, **When** FactionGraph edge author is attempted via host, **Then** Unauthorized and no edge mutation
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Research integration

- World children swap / `queue_free` semantics from WorldShell research remain authoritative for regen.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. **Paint** secondary **3.1** then tertiary **3.1.1** (this wave).
2. Next paint cursor: **3.1.2** Weather.

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **3.1**.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
