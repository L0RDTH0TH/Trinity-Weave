---
title: Phase 4.2.3 — DM Rail Chrome and DMRailUXContract (Execution)
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_collaborative_table_agency
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
- phase-4
- dm-rail-ux
- rail-chrome
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5]]'
- '[[ux_collaborative_table_agency]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.2.3 — DM Rail Chrome and DMRailUXContract (Execution)

Execution tertiary: **DMRailUXContract** — rail chrome order FP→WorldCam→MapCam→SensoriumAttach + blocked messaging on TransitionGuardRegistry fail. Tertiary: DM rail chrome + DMRailUXContract. **No Half B.** L5/SERIES are **read-only advisory feedstock** — non-silent `blocked_reason` / `guard_id` chrome enables DM rail vs player FP; never silent noop; chrome does not grant world-author.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Rail chrome + non-silent blocked_reason ([[conceptual 4.2.3]]) |
| Inspiration / L5 bar (advisory) | show_blocked(guard_id); non-silent blocked_reason; rail chrome ≠ WorldState authority; DM rail vs FP mode-switch surfacing |
| Inspiration (studied) | (1) Conceptual 4.2.3. (2) Execution 4.2 / 4.2.1 guards. (3) PresentationShell mode-switch (4.1) |
| L5 / package crosswalk | phase-aligned `[[ux_collaborative_table_agency]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted UX contract + PresentationShell chrome hooks |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_collaborative_table_agency` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.2.3 + rollup |
| `dispatch_scope` | Execution tertiary **4.2.3** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_collaborative_table_agency` |
| Label | Collaborative table agency / shared session surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Ui.DmRailChrome` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | single player owns all agency; silent seat spoof |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `hud_honesty` | `DMRailUXContract` + RailChromePresenter | DevLeakageGuard fail → Unavailable | chrome layers |
| blocked reason | `BlockedReasonSurface` | silent block forbidden | readable blocked_reason |
| mode affordance | `ModeSwitchAffordance` | wrong seat → Unauthorized | affordance state |
| feedback channel | Presentation only | chrome ≠ Simulation writer | UI residue only |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.DmRailChrome` |
| `stack-vtt-overlays` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.DmRailChrome` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.DmRailChrome` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `DMRailUXContract` | Rail order + blocked messaging + mode-switch affordances |
| `RailChromePresenter` | PresentationShell chrome binding |
| `BlockedReasonSurface` | Map guard_id → operator-visible string |
| `ModeSwitchAffordance` | Emit request into DMPerspectiveCoordinator |

## Interfaces

```text
DMRailUXContract (RefCounted):
  + rail_order() -> Array  # [PLAYER_FP, DM_WORLD, DM_MAP, DM_SENSORIUM_ATTACH]
  + show_blocked(guard_id: StringName, reason: String) -> void
  + clear_blocked() -> void
  + request_mode_switch(to_mode: int) -> Error
  + set_coordinator(coord: Node) -> void
  signals: blocked_shown(guard_id, reason)
  signals: mode_switch_requested(to_mode)

BlockedReasonSurface (RefCounted):
  + format(guard_id: StringName) -> String
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: chrome surfaces illegal transitions — never invent silent OK.
# Players do not author world: rail chrome is Presentation UX only.
# DM rail vs player FP: show_blocked(guard_id) on TransitionGuardRegistry fail.
# Agency: chrome does not grant dominate / world-author — AgencyEnvelope is 4.3.
# ===========================================================

# 4.2.3 — DMRailUXContract / rail chrome (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
# Reject: MapAnnotationEnvelope ownership (4.2.2); guard predicates (4.2.1);
#         AgencyEnvelope persistence (4.3); Camera3D ownership.

class_name DMRailUXContract
extends RefCounted

signal blocked_shown(guard_id, reason)
signal mode_switch_requested(to_mode)

var _coord: Node = null  # DMPerspectiveCoordinator
var _reason_fmt: BlockedReasonSurface = BlockedReasonSurface.new()
var _last_blocked: StringName = &""

func rail_order() -> Array:
	return [
		PerspectiveMode.PLAYER_FP,
		PerspectiveMode.DM_WORLD,
		PerspectiveMode.DM_MAP,
		PerspectiveMode.DM_SENSORIUM_ATTACH,
	]

func set_coordinator(coord: Node) -> void:
	_coord = coord

func show_blocked(guard_id: StringName, reason: String) -> void:
	_last_blocked = guard_id
	var text: String = reason if reason != "" else _reason_fmt.format(guard_id)
	blocked_shown.emit(guard_id, text)
	# PresentationShell chrome binds to blocked_shown — never silent

func clear_blocked() -> void:
	_last_blocked = &""

func request_mode_switch(to_mode: int) -> Error:
	mode_switch_requested.emit(to_mode)
	if _coord == null:
		return ERR_UNCONFIGURED
	return _coord.request_dm_mode(to_mode, &"rail_chrome")

# Wire: PresentationShell pick → request_mode_switch → coordinator
#        → TransitionGuardRegistry fail → show_blocked(guard_id)
#        → pass → matrix row apply (4.2 secondary)

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, stack-vtt-overlays, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Ui.DmRailChrome

// JUNIOR WORK-ORDER (ux_collaborative_table_agency): implement `Genesis.Ui.DmRailChrome` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Ui;
public interface IDmRailChrome {
    Error ApplyChrome(DmRailUXContract contract, SeatContext seat);
    // Must-fail: player seat → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.2.3-001 | Guard fail must call show_blocked — no silent noop |
| I-4.2.3-002 | Rail order matches conceptual: FP → World → Map → SensoriumAttach |
| I-4.2.3-003 | Chrome is Presentation-local; no Simulation writes |
| I-4.2.3-004 | AgencyEnvelope / persistence deferred to 4.3 |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-4-2 folder
- [x] Path-qualified conceptual_counterpart
- [x] Interfaces + pseudo for DMRailUXContract
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `DmRailChrome` mount/bootstrap fails closed on DevLeakageGuard / double-mount / wrong seat (Unavailable|AlreadyExists|Unauthorized) — row `ux_collaborative_table_agency`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** DevLeakageGuard fail, **When** RailChromePresenter mount, **Then** Unavailable
- [ ] **Given** blocked mode switch, **When** BlockedReasonSurface, **Then** readable blocked_reason (never silent block)
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
