---
title: Phase 3 — Living Simulation and Dynamic Agency (Execution)
roadmap-level: primary
phase-number: 3
subphase-index: "3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
status: active
priority: high
progress: 40
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
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-2-Off-Screen-Faction-Tribe-Activity/Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
catalog_row_ids:
- ux_living_world_continuity
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 3 — Living Simulation and Dynamic Agency (Execution)

Execution primary enrich (FAST map-gen): tick spine, off-screen deltas, DM overwrite vs re-gen policy. Parallel spine under `Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/`. **No Half B. No L5.** Secondaries **3.1 / 3.2 / 3.3** next DFS.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Persistent balanced simulation with DM authority respected ([[conceptual Phase 3]]) |
| Inspiration (studied) | (1) Conceptual Phase 3 + secondaries 3.1–3.3. (2) Execution Phase-2 SimGraphSeed / WorldEventLogInitializer. (3) WorldShell disposable container research |
| L5 / package | _(package cursor may shift off pkg_world_shell — advisory this mint)_ |
| Execution mechanism | Module map + interfaces for SimClock / tick pipeline / off-screen compiler / overwrite patch layer; detail on secondaries |
| Validation | Mint **3.1** secondary next; nested V/IRA batch-later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | _(advisory / may clear on Phase-3 package)_ |
| `package_id` | _(prior `pkg_world_shell` — Phase-3 package TBD)_ |
| `l5_path` | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual Phase 3 + 3.1–3.3 |
| `dispatch_scope` | Execution primary **Phase 3** enrich (4th deepen of tertiary wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 3.1 | Tick-Based Simulation Core | **next mint** |
| 3.2 | Off-Screen Faction/Tribe Activity | pending |
| 3.3 | DM Overwrite vs Deliberate Re-Generation | pending |
| 3.1.1–3.1.4 | SimClock, Weather, NPC Agendas, FactionGraph | after 3.1 |

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
| `ux_sim_weather_pulse` | `Genesis.Sim.ISimTickHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `ux_wa_faction_offscreen` | `Genesis.Sim.ISimTickHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `ux_wa_npc_agenda` | `Genesis.Sim.ISimTickHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `ux_canon_pipeline_feel` | `Genesis.Sim.ISimTickHost` / leaf modules | wrong seat / out of contract | lasting readable residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.ISimTickHost` |
| `stack-weather-ambience` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.ISimTickHost` |
| `stack-npc-schedules` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.ISimTickHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.ISimTickHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


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
  + window_id: StringName
  + events: Array
  + overflow_deferred: bool
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
  signals: tick_started(tick_id), tick_committed(tick_id), sim_paused(), sim_resumed()

SimTickPipeline (Node under Simulation layer — NOT Autoload world root):
  + run_tick() -> Error
  + last_record() -> CommittedTickRecord
  signals: tick_complete(record), tick_aborted(reason)

OffScreenActivityWindow (RefCounted):
  + open(player_left_at: float) -> void
  + close() -> NarrativeDelta
  signals: window_opened(), window_closed(delta_id)

DMOverwriteClass / OverwritePatchLayer (RefCounted):
  + classify(patch: Dictionary) -> StringName
  + apply(patch: Dictionary) -> Error
  signals: overwrite_applied(patch_id), regen_queued(intent_id)
```

## Pseudo-code

```pseudo
# Phase 3 primary — Living simulation spine (Godot 4 stable).
# Citations: Node children under Simulation layer; Error/OK; queue_free on regen swap.
# Reject: Autoload SimTickPipeline as world singleton; mutate CompiledWorldManifest
#         from off-screen without DryRun path; drop DMPauseGate deltas silently.

class_name SimTickPipeline
extends Node

signal tick_complete(record)
signal tick_aborted(reason)

var _clock: SimClock
var _weather: RefCounted      # WeatherEnvState — 3.1.2
var _npc: RefCounted          # NPCAgendaSubsystem — 3.1.3
var _factions: RefCounted     # FactionGraphSubsystem — 3.1.4
var _log: RefCounted          # WorldEventLog
var _pause_gate: RefCounted   # DMPauseGate — 3.3
var _tick_id: int = 0

func run_tick() -> Error:
	if _pause_gate != null and _pause_gate.is_paused():
		_pause_gate.queue_speculative({"tick": _tick_id + 1})
		return ERR_BUSY
	_tick_id += 1
	_clock.tick_started_emit(_tick_id)  # via signal on clock
	var deltas := {}
	for sub in [_weather, _npc, _factions]:
		if sub == null:
			continue
		var d: Dictionary = sub.tick(_clock.now())
		if d.get("overflow", false):
			# TickScheduler caps → defer remainder (3.1 / 3.2 contract)
			deltas[sub.get_class()] = d
			continue
		deltas[sub.get_class()] = d
	var rec := CommittedTickRecord.new()
	rec.tick_id = _tick_id
	rec.sim_time = _clock.now()
	rec.subsystem_deltas = deltas
	var err := _log.append(rec)
	if err != OK:
		tick_aborted.emit("log_append")
		return err
	tick_complete.emit(rec)
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

## Acceptance

- [x] Parallel spine path `Execution/Phase-3-…/` (primary)
- [x] Path-qualified `conceptual_counterpart` → frozen Phase 3
- [x] Module map + child index for 3.1 / 3.2 / 3.3
- [x] Interfaces + primary pseudo for SimTickPipeline / clock / overwrite hooks
- [ ] Secondary **3.1** Tick-Based Simulation Core minted
- [ ] Half B / playable ladder later
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Given** seat context allowed for `ux_living_world_continuity`, **When** junior implements `Genesis.Sim.ISimTickHost`, **Then** wrong-seat calls return unauthorized / emit blocked — never silent OK
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_living_world_continuity` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Research integration

- World children swap / `queue_free` semantics from WorldShell research remain authoritative for regen.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Mint **3.1** Tick-Based Simulation Core secondary (DFS).
2. Then **3.2** / **3.3**, then 3.1.x tertiaries.

## Status

`deepen_complete: true` for Execution **Phase 3** primary enrich. Nested V/IRA skipped (operator batch-later). Next secondary **3.1**.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
