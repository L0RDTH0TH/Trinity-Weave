---
title: Phase 6.2.4 — SimTickStub Sim Stub (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.4"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]'
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
- paint_ux_catalog
- pkg_world_shell
- roadmap
- genesis-mythos-master
- phase-6
- horizon-demo
- sim-stub
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-4-SimTickStub-Sim-Stub-Roadmap-2026-06-27-0715]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.2.4 — SimTickStub Sim Stub (Execution)

Execution tertiary: **SimTickStub** (beat 4) — on `intent_demo_interact` run **one** SimTickPipeline stand-in tick + **WorldEventLog** append → `demo_sim_tick_committed`. Prereq: 6.2.3 `demo_intent_labeled`. Respects **DMPauseGate**. Consumers: **6.2.5**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B.** L5/SERIES advisory — SimTickStub is bounded proof; not player canon author.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Single demo sim tick after intent ([[conceptual 6.2.4]]) |
| Inspiration / L5 bar (advisory) | One demo tick; RO residue ok; no player author canon |
| Inspiration (studied) | (1) Conceptual 6.2.4. (2) Execution 6.2.3. (3) SimTickPipeline / WorldEventLog / SimClock (3.1). (4) DMPauseGate |
| L5 / package crosswalk | phase-aligned `[[ux_living_world_continuity]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Stub Node; ≤1 tick; log append; session signal |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2.4 |
| `dispatch_scope` | Execution tertiary **6.2.4** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.SimTickStub` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_sim_weather_pulse` (bounded) | `ISimTickHost.Tick` once → weather module | second tick → Bug | WorldEventLog row |
| living continuity proof | SimTickStub.commit_one_tick | DMPauseGate → Busy | demo_sim_tick_committed |
| overflow honesty | TickScheduler deferred | never silent truncate | catchup_deferred signal |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.SimTickStub` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.SimTickStub` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SimTickStub` | awaiting_intent → tick_pending → committing → committed \| paused \| blocked |
| `DemoTickRunner` | One-shot stand-in for SimTickPipeline |
| `WorldEventLogAppender` | Append `demo_interact_observed` |
| `DMPauseGateListener` | Pause path without commit |

## Interfaces

```text
SimTickStub (Node):
  + arm_after_intent(intent: Dictionary) -> Error
  + commit_one_tick() -> Error
  + last_event_id() -> StringName
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: demo_sim_tick_committed(event_id), demo_sim_tick_paused(code), demo_sim_tick_blocked(code)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# Seats: one demo tick under current FP session — refuse free author.
# Players do not author world: stub tick is bounded proof, not canon invent.
# DM rail vs player FP: still pre-DM-cam; pause gates apply if DM later.
# Agency: sim tick does not grant DOMINATE.
# ===========================================================

# 6.2.4 — SimTickStub (Godot 4 stable).
# Citations: Node; Dictionary; StringName; Error/OK; signals.
# Reject: multi-tick loops; OffScreen/full SimTickPipeline; commit without
#         intent_labeled; Half B/L5.

class_name SimTickStub
extends Node

signal demo_sim_tick_committed(event_id)
signal demo_sim_tick_paused(code)
signal demo_sim_tick_blocked(code)

enum State { AWAITING_INTENT, TICK_PENDING, COMMITTING, COMMITTED, PAUSED, BLOCKED }
var _state: State = State.AWAITING_INTENT
var _intent: Dictionary = {}
var _last_event: StringName = &""
var _ticks_done: int = 0

var _armed_intent: Dictionary = {}

func run_beat() -> Error:
	var err := arm_after_intent(_armed_intent)
	if err != OK:
		return err
	return commit_one_tick()

func arm_after_intent(intent: Dictionary) -> Error:
	if intent.is_empty():
		_block(&"missing_intent")
		return ERR_INVALID_PARAMETER
	_intent = intent
	_state = State.TICK_PENDING
	return OK

func commit_one_tick() -> Error:
	if _state != State.TICK_PENDING:
		_block(&"bad_state")
		return ERR_UNAVAILABLE
	if _dm_paused():
		_state = State.PAUSED
		demo_sim_tick_paused.emit(&"dm_pause")
		return ERR_BUSY
	if _ticks_done >= 1:
		_block(&"tick_cap")
		return ERR_ALREADY_EXISTS
	_state = State.COMMITTING
	_last_event = &"demo_interact_observed"
	# WorldEventLog.append(_last_event, _intent) — stand-in only
	_ticks_done = 1
	_state = State.COMMITTED
	demo_sim_tick_committed.emit(_last_event)
	return OK

func _dm_paused() -> bool:
	return false

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	demo_sim_tick_blocked.emit(code)

# === WEAVE C# / .NET (Godot 4.6.3) — ISimTickHost ===
# Manifest: stack-simulation-tick, engine-godot-463-dotnet | Catalog: ux_living_world_continuity
# GAP4: demo stub *behavior* (≤1 tick) — types = Genesis.Sim.ISimTickHost (Phase 3.1), not DemoSimClock
# Index: [[Docs/SeamRegistry-CSharp-Host-Index]] §B2
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

namespace Genesis.Demo;
public sealed partial class SimTickStub : Node {
    private ISimTickHost _sim = null!; // inject Phase-3.1 host
    private int _ticks;
    public Error CommitOneTick(SimSnapshot snap) {
        if (_ticks >= 1) return Error.Bug;
        var err = _sim.Tick(snap.SimTime, snap);
        if (err != Error.Ok) return err;
        _ticks++;
        return Error.Ok;
    }
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.4-001 | arm_after_intent requires demo_intent_labeled payload |
| I-6.2.4-002 | At most one tick commit per armed intent |
| I-6.2.4-003 | DMPauseGate yields paused — no silent commit |
| I-6.2.4-004 | demo_sim_tick_committed is the sole beat-4 exit signal |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.4
- [x] Interfaces + tertiary pseudo for SimTickStub
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `SimTickStub` wrong-seat → Unauthorized; demo stub_only must not satisfy `ICampaignCapableDoDGate` alone — row `ux_living_world_continuity`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** second SimTickStub commit in demo one-shot, **When** Tick, **Then** Bug
- [ ] **Given** DMPauseGate, **When** commit_one_tick, **Then** Busy and no demo_sim_tick_committed
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.2.5**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
