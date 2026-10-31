---
title: Phase 6.1 — Factory Phase 0 Presentation Shell (Execution)
roadmap-level: secondary
phase-number: 6
subphase-index: "6.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
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
handoff_readiness: 72
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
- factory
- presentation-shell
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5]]'
- '[[ux_collaborative_table_agency]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.1 — Factory Phase 0 Presentation Shell (Execution)

> **Stock Godot FPS (mandatory before Code-Exhibit player/camera):** [[Godot-Implementation-Decision-Matrix]] + [[Godot-Stock-Patterns]]. Shell mounts PlayRegion sockets and reflects mode chrome — it does **not** implement walk/look. Seats later swap cameras + enable/disable stock FPS only.

Execution secondary: **PresentationShellManifest** + **LaunchFlowController** + **DevLeakageGuard** + **PlayRegionHost** + **HUDLayerStack** + **KinestheticHonestyChecklist**. Factory spine only — not 6.2 demo. Parallel spine under `Execution/Phase-6-…/Phase-6-1-…/`. **No Half B.** L5/SERIES advisory — factory Phase-0 shell enables seat-safe launch; HUD is Presentation only.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Launch → PlayRegion → HUD factory shell ([[conceptual 6.1]]) |
| Inspiration / L5 bar (advisory) | Session bootstrap; DevLeakageGuard; kinesthetic honesty; seats before demo |
| Inspiration (studied) | (1) Conceptual 6.1 + 6.1.1–6.1.3. (2) Execution Phase-6 primary. (3) 1.1 Presentation / InputIntent. (4) 4.1 PerspectiveEnvelope (RO mode reflect) |
| L5 / package crosswalk | phase-aligned `[[ux_collaborative_table_agency]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Node host + RefCounted controllers; KH checklist gates |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_collaborative_table_agency` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.1 |
| `dispatch_scope` | Execution secondary **6.1** mint (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 6.1.1 | Launch Flow / DevLeakageGuard Session Bootstrap | **minted** |
| 6.1.2 | PlayRegionHost Mount Lifecycle | **minted** |
| 6.1.3 | HUDLayerStack / Kinesthetic Honesty Checklist | **minted** |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_collaborative_table_agency` |
| Label | Collaborative table agency / shared session surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Ui.IUiHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | single player owns all agency; silent seat spoof |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| launch | `LaunchFlowController` | DevLeakageGuard fail → Unavailable | session handle |
| mount | `PlayRegionHost` | double-mount → AlreadyExists | mounted region |
| `hud_honesty` | `HUDLayerStack` + KinestheticHonestyChecklist | leakage → Unavailable | layer stack |
| shared_table | IUiHost seat inject | missing seat → degraded | SeatContext |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.IUiHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.IUiHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility | Owner tertiary |
|--------|----------------|----------------|
| `LaunchFlowController` | Bootstrap + DevLeakageGuard → PresentationSessionHandle | 6.1.1 |
| `DevLeakageGuard` | Fail-closed on leak paths | 6.1.1 |
| `PlayRegionHost` | Single viewport + sockets | 6.1.2 |
| `HUDLayerStack` | Base/Mode/Context/Transient | 6.1.3 |
| `KinestheticHonestyChecklist` | KH-6.1-001–004 gates | 6.1.3 |

## Interfaces

```text
PresentationSessionHandle (RefCounted):
  + session_id: StringName
  + shell_id: StringName
  + to_dict() -> Dictionary

LaunchFlowController (RefCounted):
  + run_with_dev_leakage_guard() -> Error
  + shell_manifest() -> PresentationShellManifest
  + play_region_host() -> PlayRegionHost
  + session_handle() -> PresentationSessionHandle

DevLeakageGuard (RefCounted):
  + check(paths: Array) -> Error
  + is_clean() -> bool

PlayRegionHost (Node):
  + ensure_single_viewport() -> Error
  + bind_socket(name: StringName, node: Node) -> Error
  + mount_demo(demo: HorizonDemoManifest) -> Error
  signals: presentation_play_region_ready(host_id)

HUDLayerStack (Node):
  + set_layer(layer: StringName, visible: bool) -> Error
  + reflect_mode(mode: int) -> Error  # RO from PerspectiveEnvelope — never drives ModeTransitionGraph
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: shell mounts Presentation seats — refuse Dev leakage into production authority.
# Players do not author world: HUD/PlayRegion are Presentation, not WorldState writers.
# DM rail vs player FP: shell ready for both; default remains FP-safe until demo/DM cue.
# Agency: no dominate until explicit demo/agency path (P4/P5/6.2).
# ===========================================================

# 6.1 — Factory Phase 0 Presentation Shell (Godot 4 stable).
# Citations: Node; Viewport; Error/OK; StringName; signals.
# Reject: driving ModeTransitionGraph from HUD; second PlayRegionHost;
#         Simulation Autoload; 6.2 demo beats inside factory attestation.

class_name LaunchFlowController
extends RefCounted

var _guard: DevLeakageGuard
var _shell: PresentationShellManifest
var _host: PlayRegionHost
var _handle: PresentationSessionHandle

func run_with_dev_leakage_guard() -> Error:
	var err: Error = _guard.check(_shell.leak_scan_paths())
	if err != OK:
		return err
	err = _host.ensure_single_viewport()
	if err != OK:
		return err
	_handle = PresentationSessionHandle.new()
	_handle.session_id = StringName(str(Time.get_ticks_msec()))
	_handle.shell_id = _shell.shell_id
	_host.emit_signal("presentation_play_region_ready", _host.get_instance_id())
	return OK

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Ui.IUiHost

// JUNIOR WORK-ORDER (ux_collaborative_table_agency): implement `Genesis.Ui.IUiHost` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Ui;
// Index B5
public interface IUiHost {
    Error MountPresentation(Node shell, SeatContext seat);
    // Must-fail: DevLeakageGuard fail → Unavailable
}

```

## Validation signals

| Signal | Meaning |
|--------|---------|
| `presentation_play_region_ready` | Host ready for 6.2 mount |
| DevLeakageGuard fail | Launch aborted |
| Duplicate viewport | `ensure_single_viewport` → ERR |

## Rejects

- HUD driving ModeTransitionGraph
- Factory attestation requiring demo.loop_complete
- Half B / L5

## Junior acceptance / verify (weave)

- [ ] **Verify** `IUiHost` mount/bootstrap fails closed on DevLeakageGuard / double-mount / wrong seat (Unavailable|AlreadyExists|Unauthorized) — row `ux_collaborative_table_agency`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** DevLeakageGuard fail, **When** LaunchFlowController.Begin, **Then** Unavailable
- [ ] **Given** PlayRegionHost already mounted, **When** Mount again, **Then** AlreadyExists

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.1.1**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

## Next

Phase-6 execution subtree **complete on disk** (6.1–6.4; 6.1.1–6.1.3; 6.2.1–6.2.8). Batch validate/IRA only. Cursor: `map_gen_complete` / `6.2.8`. **No Half B.** L5/SERIES advisory (see UX Catalog paint).

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
