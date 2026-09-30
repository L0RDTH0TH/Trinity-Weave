---
title: Phase 3.1 — Tick-Based Simulation Core (Execution)
roadmap-level: secondary
phase-number: 3
subphase-index: "3.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_living_world_continuity
priority: high
progress: 70
handoff_readiness: 78
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-3
- tick-core
- simulation
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Generation-Pipeline-Stages/Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 3.1 — Tick-Based Simulation Core (Execution)

Execution secondary: authoritative **SimClock** + **TickScheduler** + **SimTickPipeline** (weather → NPC → faction → consequence) + **WorldStateCommitter** + **WorldEventLog** commit, independent of Presentation. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — ToneProfileConsequenceWeights on weather/NPC + lasting WorldState commit **enable** persistent living world.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Tick loop independent of rendering; DM pause respected |
| Inspiration / L5 bar (advisory) | Tone-weighted weather/NPC ticks; lasting WorldState+log; overflow residue deferred not truncated |
| Inspiration (studied) | (1) Conceptual 3.1 + rollup. (2) Execution Phase-3 primary. (3) Phase-2 SimGraphSeed / WorldEventLogInitializer. |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + pseudo for clock, scheduler, pipeline, commit, tone consequence weights |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 3.1 + tertiaries 3.1.1–3.1.4 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Sim.SimTickHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| tick advance | `SimTickPipeline` + `SimClock` | `DMPauseGate` → Busy (no commit) | tick_id advanced |
| subsystem dispatch | weather/NPC/faction slots under host | wrong slot_id → InvalidParameter | per-slot TickDelta |
| overflow honesty | `TickScheduler` catchup | never silent truncate | catchup_deferred signal |
| lasting costs | `ConsequenceResolver` → WorldEventLog | Presentation must not write log | lasting cost row |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.SimTickHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.SimTickHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility | Owner tertiary |
|--------|----------------|----------------|
| `SimClock` | Authoritative sim time, step modes, pause | 3.1.1 |
| `TickScheduler` | Frame-budget caps + catchup deferral | 3.1.1 |
| `DMPauseGate` | Pause-first; speculative queue (handoff → 3.3) | 3.1 / 3.3 |
| `SimTickPipeline` | Ordered subsystem dispatch under Simulation Node | 3.1 |
| `WeatherEnvState` | First pipeline slot | 3.1.2 |
| `NPCAgendaSubsystem` | Second pipeline slot | 3.1.3 |
| `FactionGraphSubsystem` | Third pipeline slot | 3.1.4 |
| `ConsequenceResolver` | Tone-weighted consequence merge | 3.1 |
| `ToneProfileConsequenceWeights` | Weights from Phase-2 tone fingerprint | 3.1 |
| `WorldStateCommitter` | Atomic WorldState apply after tick | 3.1 |
| `WorldEventLog` | Append-only CommittedTickRecord | 3.1 (from 2.1 init) |
| `SimGraphSeed` | Bootstrap graph from Phase-2 compile | import 2.1 |

## Interfaces

```text
enum TickStepMode { FIXED_DT, VARIABLE_CAPPED, CATCHUP_BATCH }

CommittedTickRecord (RefCounted):
  + tick_id: int
  + sim_time: float
  + step_mode: int
  + subsystem_deltas: Dictionary
  + provenance: Dictionary
  + to_dict() -> Dictionary

TickBudgetManifest (RefCounted):
  + max_ticks_per_frame: int
  + max_subsystem_ms: float
  + catchup_cap: int
  + to_dict() -> Dictionary

SimClock (RefCounted):
  + now() -> float
  + tick_id() -> int
  + step_mode() -> int
  + pause() -> void
  + resume() -> void
  + advance(dt: float) -> Error
  signals: tick_started(tick_id), tick_advanced(tick_id, sim_time)
  signals: sim_paused(), sim_resumed()

TickScheduler (RefCounted):
  + bind_budget(manifest: TickBudgetManifest) -> void
  + can_run_tick() -> bool
  + record_subsystem_cost(slot: StringName, ms: float) -> void
  + defer_catchup(reason: StringName) -> void
  signals: catchup_deferred(reason), budget_exhausted(frame_id)

ISimSubsystem (RefCounted):
  + slot_id() -> StringName
  + tick(sim_time: float, snapshot: Dictionary) -> Dictionary
  # returns delta Dictionary; may set overflow:true

SimTickPipeline (Node under Simulation layer — NOT Autoload):
  + bind_subsystems(ordered: Array) -> void
  + run_tick() -> Error
  + last_record() -> CommittedTickRecord
  signals: tick_complete(record), tick_aborted(reason)

ConsequenceResolver (RefCounted):
  + resolve(deltas: Dictionary, weights: Dictionary) -> Dictionary
  signals: consequences_ready(bundle)

WorldStateCommitter (RefCounted):
  + commit(resolved: Dictionary, record: CommittedTickRecord) -> Error
  signals: world_state_committed(tick_id)

WorldEventLog (RefCounted):
  + append(record: CommittedTickRecord) -> Error
  signals: tick_logged(tick_id)
```

## Pseudo-code

```pseudo
# Phase 3.1 — Tick-Based Simulation Core (Godot 4 stable).
# Citations: Node under Simulation layer; RefCounted; Error/OK; signals.
#
# === JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# Tone-weighted living world: ConsequenceResolver.resolve MUST pass ToneProfileConsequenceWeights
#   (weather/NPC/faction deltas inherit Phase-2 fingerprint — never invent unweighted facts).
# Lasting world state: WorldStateCommitter.commit AND WorldEventLog.append — both required.
# Off-screen residue: overflow → TickScheduler.defer_catchup — NEVER silent truncate.
# DM-retconnable: is_paused / may_advance BEFORE clock.advance; queue_speculative on hold.
# Players do not author ticks — Presentation consumes tick_complete async only.
# ===========================================================

class_name SimTickPipeline
extends Node

signal tick_complete(record)
signal tick_aborted(reason)

var _clock: SimClock
var _scheduler: TickScheduler
var _pause_gate: RefCounted          # DMPauseGate (3.3)
var _subs: Array = []                # ISimSubsystem ordered weather→npc→faction
var _resolver: ConsequenceResolver
var _weights: RefCounted             # ToneProfileConsequenceWeights — living-world tone
var _committer: WorldStateCommitter  # lasting WorldState
var _log: WorldEventLog              # durable WorldEventLog rows (lasting costs)
var _snapshot_ro: Callable

func run_tick() -> Error:
	# JUNIOR WORK-ORDER: DM pause = retconnable hold — queue, do not invent
	if _pause_gate != null and _pause_gate.is_paused():
		_pause_gate.queue_speculative({"pending_tick": _clock.tick_id() + 1})
		return ERR_BUSY
	if not _scheduler.can_run_tick():
		# JUNIOR WORK-ORDER: frame-budget residue → defer catchup (off-screen path)
		_scheduler.defer_catchup(&"frame_budget")
		return ERR_BUSY
	if _pause_gate != null and not _pause_gate.may_advance():
		return ERR_BUSY
	var err := _clock.advance(_clock_dt())
	if err != OK:
		tick_aborted.emit("clock_advance")
		return err
	_clock.emit_signal("tick_started", _clock.tick_id())
	var snapshot: Dictionary = _snapshot_ro.call()
	var deltas := {}
	for sub in _subs:
		var t0 := Time.get_ticks_msec()
		var d: Dictionary = sub.tick(_clock.now(), snapshot)
		_scheduler.record_subsystem_cost(sub.slot_id(), float(Time.get_ticks_msec() - t0))
		deltas[sub.slot_id()] = d
		if d.get("overflow", false):
			# JUNIOR WORK-ORDER: off-screen / budget overflow → defer, never truncate
			_scheduler.defer_catchup(sub.slot_id())
	# JUNIOR WORK-ORDER: tone-weighted merge — living world continuity
	var resolved := _resolver.resolve(deltas, _weights.to_dict() if _weights else {})
	var rec := CommittedTickRecord.new()
	rec.tick_id = _clock.tick_id()
	rec.sim_time = _clock.now()
	rec.step_mode = _clock.step_mode()
	rec.subsystem_deltas = deltas
	rec.provenance = {"resolved_keys": resolved.keys()}
	# JUNIOR WORK-ORDER: lasting world — commit + log both required
	err = _committer.commit(resolved, rec)
	if err != OK:
		tick_aborted.emit("commit")
		return err
	err = _log.append(rec)
	if err != OK:
		tick_aborted.emit("log_append")
		return err
	tick_complete.emit(rec)  # Presentation async only
	return OK

# Pipeline order: weather → npc_agendas → faction_graph → resolve → commit → log.
# SimGraphSeed (Phase 2.1) seeds registries once.

# === WEAVE C# / .NET (Godot 4.6.3) — ISimTickHost ===
# Manifest: stack-simulation-tick, engine-godot-463-dotnet | Catalog: ux_living_world_continuity
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
| I-3.1-001 | SimTickPipeline is a Simulation-layer Node — never Autoload world root |
| I-3.1-002 | DMPauseGate pause → queue speculative; never advance + commit while paused |
| I-3.1-003 | TickScheduler overflow → `sim.catchup_deferred` — no silent truncate |
| I-3.1-004 | Presentation must not block `run_tick`; consume `tick_complete` async |
| I-3.1-005 | Precedence on merge: canon > faction > NPC > weather (ConsequenceResolver) |
| I-3.1-006 | WorldEventLog append is required for every successful commit |
| I-3.1-007 | **L5:** ToneProfileConsequenceWeights + lasting commit/log preserve living-world continuity |

## Acceptance

- [x] Parallel spine `Execution/Phase-3-…/Phase-3-1-…/`
- [x] Path-qualified `conceptual_counterpart` → frozen 3.1
- [x] Module map + child index for 3.1.1–3.1.4
- [x] Interfaces + secondary pseudo for SimTickPipeline / clock / commit
- [x] Tertiary **3.1.1** SimClock/TickScheduler minted
- [x] Tertiary **3.1.2** Weather minted
- [x] Tertiary **3.1.3** NPC Agendas minted
- [x] Tertiary **3.1.4** FactionGraph minted
- [x] **UX Catalog paint** — L5 tone-weighted / lasting / residue as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `SimTickHost` tick/admit path fails closed (Unauthorized|InvalidParameter|Busy) on wrong seat / null input — row `ux_living_world_continuity`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** DMPauseGate asserted, **When** SimTickPipeline.Tick, **Then** Busy and tick_id unchanged
- [ ] **Given** TickScheduler over budget, **When** catchup runs, **Then** catchup_deferred fires and no silent truncation of subsystem deltas
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Research integration

- WorldShell / SceneTree citations remain authoritative for Simulation-layer Node placement and regen swap — not for Autoload tick roots.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. **Paint** tertiary **3.1.1** (this wave).
2. Next paint cursor: **3.1.2** Weather.

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **3.1.1**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
