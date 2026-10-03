---
title: Phase 3.1.1 — SimClock and TickScheduler Policy (Execution)
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roadmap-2026-06-29-2205]]'
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
- sim-clock
- tick-scheduler
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roadmap-2026-06-29-2205]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 3.1.1 — SimClock and TickScheduler Policy (Execution)

Execution tertiary: **SimClockPolicyRegistry**, **TickBudgetManifest**, **CatchupDeferralPolicy**, **SessionTimeSyncBinding**, **DMPauseGate** clock integration. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — pause-first advance + catchup deferral **enable** DM-retconnable living-world continuity and off-screen residue (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Step-mode registry + frame-budget policy for authoritative tick |
| Inspiration / L5 bar (advisory) | DM-retconnable pause before advance; off-screen/budget residue via catchup_deferred (never silent); lasting tick_id/sim_time authority |
| Inspiration (studied) | (1) Conceptual 3.1.1 + rollup. (2) Execution 3.1 SimClock/TickScheduler stubs. (3) Phase-1.3 provenance. |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + pseudo for policy registry → budget → pause-first advance |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 3.1.1 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Sim.SimClock` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| clock authority | `SimClock.Advance` | pause via `DMPauseGateClockBridge` → Busy | tick_id / sim_time |
| budget / catchup | `TickBudgetManifest` + `CatchupDeferralPolicy` | over budget → defer (no silent drop) | catchup_deferred |
| session UX sync | `SessionTimeSyncBinding` (non-authority) | must not override SimClock | wall-clock hint only |
| weather/faction/NPC | **not owned here** — dispatch leaves | SimClock ≠ content writer | (delegate to 3.1.2–3.1.4) |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.SimClock` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.SimClock` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SimClockPolicyRegistry` | Canonical step-mode + pause bindings |
| `TickBudgetManifest` | max ticks/frame, subsystem ms, catchup cap |
| `CatchupDeferralPolicy` | When backlog exceeds cap → defer + signal |
| `SessionTimeSyncBinding` | Optional wall-clock sync for session UX (not authority) |
| `DMPauseGateClockBridge` | Pause-first gate before any `advance` |
| `SimClock` | Authoritative time + tick_id (refined from 3.1) |
| `TickScheduler` | Budget enforcement per frame |

## Interfaces

```text
enum TickStepMode { FIXED_DT, VARIABLE_CAPPED, CATCHUP_BATCH }

SimClockPolicyBinding (RefCounted):
  + policy_id: StringName
  + step_mode: int
  + fixed_dt: float
  + max_dt: float
  + enabled: bool
  + to_dict() -> Dictionary

TickBudgetManifest (RefCounted):
  + max_ticks_per_frame: int
  + max_subsystem_ms: float
  + catchup_cap: int
  + to_dict() -> Dictionary

SimClockPolicyRegistry (RefCounted):
  + register(binding: SimClockPolicyBinding) -> Error
  + active() -> SimClockPolicyBinding
  + set_active(policy_id: StringName) -> Error
  signals: policy_changed(policy_id)

CatchupDeferralPolicy (RefCounted):
  + evaluate(backlog: int, manifest: TickBudgetManifest) -> Dictionary
  # { defer:bool, reason:StringName, emit_bus:bool }

SessionTimeSyncBinding (RefCounted):
  + wall_offset_sec: float
  + enabled: bool
  + to_dict() -> Dictionary
  # Advisory only — never overrides SimClock.now() authority

DMPauseGateClockBridge (RefCounted):
  + may_advance() -> bool
  + on_blocked() -> void   # queues speculative via DMPauseGate
  signals: advance_blocked(reason)

SimClock (RefCounted):  # refined
  + bind_policy(registry: SimClockPolicyRegistry) -> void
  + now() -> float
  + tick_id() -> int
  + step_mode() -> int
  + pause() -> void
  + resume() -> void
  + advance(dt: float) -> Error
  signals: tick_started(tick_id), tick_advanced(tick_id, sim_time)
  signals: sim_paused(), sim_resumed()

TickScheduler (RefCounted):  # refined
  + bind_budget(manifest: TickBudgetManifest) -> void
  + bind_deferral(policy: CatchupDeferralPolicy) -> void
  + begin_frame() -> void
  + can_run_tick() -> bool
  + record_subsystem_cost(slot: StringName, ms: float) -> void
  + note_backlog(n: int) -> void
  + defer_catchup(reason: StringName) -> void
  signals: catchup_deferred(reason), budget_exhausted(frame_id)
```

## Pseudo-code

```pseudo
# 3.1.1 — SimClock + TickScheduler policy (Godot 4 stable).
# Citations: RefCounted, Error/OK, Time.get_ticks_msec, signals.
#
# === JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# DM-retconnable: may_advance BEFORE advance; on_blocked queues speculative — never invent.
# Off-screen residue: catchup over cap → defer_catchup + sim.catchup_deferred — NEVER silent.
# Lasting world time: SimClock sole authority for now()/tick_id; wall sync advisory only.
# Players do not author ticks — SessionTimeSyncBinding never writes _sim_time.
# ===========================================================

class_name TickScheduler
extends RefCounted

signal catchup_deferred(reason)
signal budget_exhausted(frame_id)

var _manifest: TickBudgetManifest
var _deferral: CatchupDeferralPolicy
var _ticks_this_frame: int = 0
var _frame_id: int = 0
var _backlog: int = 0
var _bus: Object   # sim.* emitter (1.1)

func begin_frame() -> void:
	_frame_id += 1
	_ticks_this_frame = 0

func can_run_tick() -> bool:
	if _ticks_this_frame >= _manifest.max_ticks_per_frame:
		budget_exhausted.emit(_frame_id)
		return false
	var ev := _deferral.evaluate(_backlog, _manifest)
	if ev.get("defer", false):
		# JUNIOR WORK-ORDER: off-screen / catchup residue — defer, never truncate
		defer_catchup(ev.get("reason", &"catchup_cap"))
		return false
	return true

func defer_catchup(reason: StringName) -> void:
	catchup_deferred.emit(reason)
	if _bus:
		_bus.emit_signal("sim_catchup_deferred", reason, _backlog)


class_name SimClock
extends RefCounted

signal tick_started(tick_id)
signal tick_advanced(tick_id, sim_time)
signal sim_paused()
signal sim_resumed()

var _registry: SimClockPolicyRegistry
var _pause_bridge: DMPauseGateClockBridge
var _sim_time: float = 0.0
var _tick_id: int = 0
var _paused: bool = false

func advance(dt: float) -> Error:
	# JUNIOR WORK-ORDER: DM pause = retconnable hold — block + queue, do not invent
	if _paused or (_pause_bridge and not _pause_bridge.may_advance()):
		if _pause_bridge:
			_pause_bridge.on_blocked()
		return ERR_BUSY
	var b := _registry.active()
	var use_dt := dt
	match b.step_mode:
		TickStepMode.FIXED_DT:
			use_dt = b.fixed_dt
		TickStepMode.VARIABLE_CAPPED:
			use_dt = minf(dt, b.max_dt)
		TickStepMode.CATCHUP_BATCH:
			use_dt = b.fixed_dt
	_tick_id += 1
	_sim_time += use_dt  # JUNIOR WORK-ORDER: lasting world time authority
	tick_started.emit(_tick_id)
	tick_advanced.emit(_tick_id, _sim_time)
	return OK

func pause() -> void:
	_paused = true
	sim_paused.emit()

func resume() -> void:
	_paused = false
	sim_resumed.emit()

# Pipeline MUST: can_run_tick → may_advance → clock.advance (parent 3.1).
# SessionTimeSyncBinding is UX-only — never writes _sim_time.

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
| I-3.1.1-001 | SimClock is sole authority for `now()` / `tick_id` — wall sync is advisory |
| I-3.1.1-002 | Pause-first: no `advance` while DMPauseGate / clock paused |
| I-3.1.1-003 | Catchup over cap → `sim.catchup_deferred` bus event (never silent) |
| I-3.1.1-004 | `max_ticks_per_frame` hard-stops additional advances that frame |
| I-3.1.1-005 | Provenance on committed ticks includes active `policy_id` + step_mode |
| I-3.1.1-006 | **L5:** pause-first + catchup deferral preserve DM-retconnable living-world continuity |

## Acceptance

- [x] Parallel spine under Phase-3-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 3.1.1
- [x] Module map + interfaces + pseudo for registry / budget / clock
- [x] **UX Catalog paint** — L5 pause/residue/lasting-time as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `SimClock` tick/admit path fails closed (Unauthorized|InvalidParameter|Busy) on wrong seat / null input — row `ux_living_world_continuity`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** pause via DMPauseGateClockBridge, **When** SimClock.Advance, **Then** Busy and sim_time unchanged
- [ ] **Given** TickBudgetManifest exceeded, **When** CatchupDeferralPolicy applies, **Then** deferred signal — SimClock does not write weather/faction/NPC content
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Research integration

- Simulation-layer Node placement (parent 3.1) unchanged; this tertiary is RefCounted policy — no Autoload.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Next paint cursor: **3.1.2** Weather Environmental State.

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **3.1.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
