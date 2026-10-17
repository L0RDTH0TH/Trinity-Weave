---
title: Phase 3.2 — Off-Screen Faction / Tribe Activity (Execution)
roadmap-level: secondary
phase-number: 3
subphase-index: "3.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-2-Off-Screen-Faction-Tribe-Activity/Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_living_world_continuity
priority: high
progress: 50
handoff_readiness: 72
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-3
- off-screen
- narrative-delta
- faction
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-2-Off-Screen-Faction-Tribe-Activity/Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-4-FactionGraph-Subsystem-Roadmap-2026-06-30-0015]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed/Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 3.2 — Off-Screen Faction / Tribe Activity (Execution)

Execution secondary: package off-screen faction/tribe evolution into **"since you left…"** narrative deltas. Owns **OffScreenActivityWindow**, **FactionGraphDeltaExtractor**, **TribeActivityScheduler**, **SinceYouLeftCompiler**, **NarrativeSurfacingPolicy**, **AbsenceCatchupBridge**, **ThreadRevealGate**, **ToneProfileNarrativeWeights**. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — off-screen residue packaging + tone-weighted severity + DM-retconnable surfacing **enable** lasting living-world continuity (tick math stays in **3.1**).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Absence window → compiled NarrativeDelta |
| Inspiration / L5 bar (advisory) | Off-screen residue → SinceYouLeft; ToneProfile narrative weights; DMPauseGate retconnable hold; never invent missing ticks |
| Inspiration (studied) | (1) Conceptual 3.2 + rollup. (2) Execution 3.1 / 3.1.4. (3) Phase-2.3 tone |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + pseudo for window → catch-up → diff → compile → route |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 3.2 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Sim.OffScreen.SinceYouLeftCompiler` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_wa_faction_offscreen` | `FactionGraphDeltaExtractor` + TribeActivityScheduler | player seat refuse compile | off-screen activity window |
| since-you-left | `SinceYouLeftCompiler` | ThreadRevealGate closed → hold | surfacing packet |
| absence catchup | `AbsenceCatchupBridge` | over budget → deferred_regions | catchup digest |
| weather/NPC agenda | **not owned** — read deltas only | compiler ≠ weather/NPC writer | narrative hints only |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-npc-schedules` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.OffScreen.SinceYouLeftCompiler` |
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.OffScreen.SinceYouLeftCompiler` |
| `stack-persistence-snapshots` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.OffScreen.SinceYouLeftCompiler` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.OffScreen.SinceYouLeftCompiler` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `OffScreenActivityWindow` | last_player_presence_tick + wall-clock absence span |
| `FactionGraphDeltaExtractor` | Diff edges/membership between CommittedTickRecord anchors |
| `TribeActivityScheduler` | Threshold rules for off-screen raids / migrations / treaties |
| `SinceYouLeftCompiler` | Merge graph delta + WorldEventLog → ranked NarrativeDelta |
| `NarrativeSurfacingPolicy` | Route: auto_brief / dm_queue / suppress |
| `AbsenceCatchupBridge` | Read 3.1 TickScheduler catch-up caps — packaging only |
| `ThreadRevealGate` | LoreHookRegistry sim-active vs hooked-only |
| `ToneProfileNarrativeWeights` | Severity → tone from Phase-2.3 bundle |

## Interfaces

```text
NarrativeDelta (RefCounted):
  + delta_id: StringName
  + severity: int
  + faction_ids: PackedStringArray
  + summary_key: StringName
  + route: StringName   # auto_brief | dm_queue | suppress
  + provenance: Dictionary
  + to_dict() -> Dictionary

OffScreenActivityWindow (RefCounted):
  + span(session: Dictionary) -> Dictionary  # {tick_depart, tick_return, wall_dt}
  + mark_presence(tick_id: int) -> void

FactionGraphDeltaExtractor (RefCounted):
  + diff(tick_depart: int, tick_return: int, log: RefCounted) -> Dictionary
  # reads FactionGraphRegistry snapshots via CommittedTickRecord — never re-runs 3.1.4 tick

TribeActivityScheduler (RefCounted):
  + armed_events(window: Dictionary) -> Array

SinceYouLeftCompiler (RefCounted):
  + compile(graph_delta: Dictionary, log: RefCounted, weights: Dictionary) -> Array

NarrativeSurfacingPolicy (RefCounted):
  + split(items: Array, reveal_gate: RefCounted) -> Dictionary
  # {auto_brief:Array, dm_queue:Array, suppress:Array}

AbsenceCatchupBridge (RefCounted):
  + request_or_read(window: Dictionary) -> Dictionary
  # overflow → deferred narrative; never invents missing ticks

ThreadRevealGate (RefCounted):
  + may_reveal(hook_id: StringName, mode: StringName) -> bool

ToneProfileNarrativeWeights (RefCounted):
  + weight_for(severity: int) -> float
  + to_dict() -> Dictionary

OffScreenNarrativeSubsystem (RefCounted):
  + on_player_return(session: Dictionary) -> Dictionary
  signals: since_you_left_compiled(bundle)
```

## Pseudo-code

```pseudo
# 3.2 — Off-screen narrative packaging (Godot 4 stable).
# Citations: RefCounted, PackedStringArray, signals.
#
# === JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# Off-screen residue: diff CommittedTickRecord anchors — NEVER re-run 3.1.4 tick to invent history.
# Tone-weighted: SinceYouLeftCompiler uses ToneProfileNarrativeWeights.
# Lasting world: WorldEventLog RO anchors required for compile.
# DM-retconnable: DMPauseGate pause → dm_queue only (no auto_brief invent).
# Catchup residue: AbsenceCatchupBridge overflow → deferred flag — NEVER fabricate missing ticks.
# Players do not author narrative deltas.
# ===========================================================

class_name OffScreenNarrativeSubsystem
extends RefCounted

signal since_you_left_compiled(bundle)

var _window: OffScreenActivityWindow
var _extractor: FactionGraphDeltaExtractor
var _tribe_sched: TribeActivityScheduler
var _compiler: SinceYouLeftCompiler
var _surfacer: NarrativeSurfacingPolicy
var _catchup: AbsenceCatchupBridge
var _reveal: ThreadRevealGate
var _tone: ToneProfileNarrativeWeights
var _log: RefCounted          # WorldEventLog — lasting
var _pause_gate: RefCounted   # DMPauseGate — 3.3

func on_player_return(session: Dictionary) -> Dictionary:
	var window: Dictionary = _window.span(session)
	var catchup: Dictionary = _catchup.request_or_read(window)
	if catchup.get("overflow", false):
		# JUNIOR WORK-ORDER: catchup residue — partial + deferred; never invent ticks
		pass
	# JUNIOR WORK-ORDER: off-screen residue from lasting log — never re-tick 3.1.4
	var graph_delta: Dictionary = _extractor.diff(
		int(window.get("tick_depart", 0)),
		int(window.get("tick_return", 0)),
		_log
	)
	graph_delta["tribe_events"] = _tribe_sched.armed_events(window)
	# JUNIOR WORK-ORDER: tone-weighted narrative severity
	var items: Array = _compiler.compile(graph_delta, _log, _tone.to_dict())
	if _pause_gate != null and _pause_gate.is_paused():
		# JUNIOR WORK-ORDER: DM-retconnable — pause auto-brief; dm_queue for 3.3 veto
		for it in items:
			it.route = &"dm_queue"
	var routed: Dictionary = _surfacer.split(items, _reveal)
	var bundle := {
		"window": window,
		"catchup": catchup,
		"routed": routed,
		"event": &"narrative.since_you_left_compiled",
	}
	since_you_left_compiled.emit(bundle)
	return bundle

# Ordering: 3.1 commits BEFORE packaging. 3.3 may veto dm_queue.

# === WEAVE C# / .NET (Godot 4.6.3) — ISimTickHost ===
# Manifest: stack-npc-schedules, stack-simulation-tick, stack-persistence-snapshots, engine-godot-463-dotnet | Catalog: ux_living_world_continuity
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
| I-3.2-001 | Never re-run 3.1.4 tick math to fill absence gaps |
| I-3.2-002 | AbsenceCatchupBridge respects TickScheduler catch-up caps |
| I-3.2-003 | DMPauseGate pause → no auto_brief; dm_queue allowed |
| I-3.2-004 | ThreadRevealGate must consult LoreHookRegistry before reveal |
| I-3.2-005 | Suppressed routes never leak into Presentation auto_brief |
| I-3.2-006 | **L5:** tone weights + lasting log + DM pause preserve living-world residue |

## Acceptance

- [x] Parallel spine `Execution/Phase-3-…/Phase-3-2-…/`
- [x] Path-qualified `conceptual_counterpart` → frozen 3.2
- [x] Module map + interfaces + pseudo for OffScreenNarrativeSubsystem
- [x] **UX Catalog paint** — L5 off-screen/tone/DM-retconnable as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `SinceYouLeftCompiler` tick/admit path fails closed (Unauthorized|InvalidParameter|Busy) on wrong seat / null input — row `ux_living_world_continuity`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player seat, **When** SinceYouLeftCompiler.Compile, **Then** Unauthorized
- [ ] **Given** ThreadRevealGate closed, **When** surfacing attempted, **Then** hold packet — no WorldState invent
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Research integration

- Presentation consumes `narrative.since_you_left_compiled` RO — Simulation owns packaging.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Next paint cursor: **3.3** DM Overwrite / Re-Gen (this wave).

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **3.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
