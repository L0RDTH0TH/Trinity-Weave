---
title: Phase 6.1.2 — PlayRegionHost Mount Lifecycle (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
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
- phase-6
- play-region
- mount-lifecycle
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5]]'
- '[[ux_collaborative_table_agency]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.1.2 — PlayRegionHost Mount Lifecycle (Execution)

Execution tertiary: **PlayRegionHost** mount + rig sockets + **PlayRegionMountReceipt** + `presentation_play_region_ready`. Prereq: 6.1.1 launch_complete. HUD → **6.1.3**. Parallel spine under `Execution/Phase-6-…/Phase-6-1-…/`. **No Half B.** L5/SERIES advisory — PlayRegionHost mounts seat sockets; FP≠DM host slots stay distinct.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Single PlayRegion mount + sockets after launch ([[conceptual 6.1.2]]) |
| Inspiration / L5 bar (advisory) | Single PlayRegion; sockets for FP/DM hosts; refuse multi-authority mount |
| Inspiration (studied) | (1) Conceptual 6.1.2. (2) Execution 6.1 / 6.1.1. (3) PerspectiveEnvelope (4.1). (4) SeamRegistry (1.3) |
| L5 / package crosswalk | phase-aligned `[[ux_collaborative_table_agency]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Node host; single-active viewport; MountContractGlue ids for 6.2/6.3 |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_collaborative_table_agency` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.1.2 |
| `dispatch_scope` | Execution tertiary **6.1.2** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_collaborative_table_agency` |
| Label | Collaborative table agency / shared session surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Ui.PlayRegionHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | single player owns all agency; silent seat spoof |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| mount | `PlayRegionHost.Mount` | double-mount → AlreadyExists | mounted region id |
| unmount | `PlayRegionHost.Unmount` | not mounted → DoesNotExist | cleared |
| lifecycle | mount contract | wrong track → Unauthorized | lifecycle audit |
| HUD | **delegate 6.1.3** | host ≠ HUD writer | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.PlayRegionHost` |
| `stack-regional-modules` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.PlayRegionHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.PlayRegionHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `PlayRegionHost` | Single viewport + socket table |
| `PlayRegionMountReceipt` | Mount id + handle echo |
| `RigSocketTable` | fp_baseline_rig, dm_worldcam_slot; mapcam stub |
| `MountLifecycle` | idle → mounting → ready \| failed |

## Interfaces

```text
PlayRegionMountReceipt (RefCounted):
  + mount_id: StringName
  + session_id: StringName
  + host_instance_id: int

PlayRegionHost (Node):
  + ensure_single_viewport() -> Error
  + mount(handle: PresentationSessionHandle) -> Error
  + receipt() -> PlayRegionMountReceipt
  + socket(name: StringName) -> Node
  signals: presentation_play_region_ready(host_id), presentation_play_region_failed(code)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: single PlayRegionHost — refuse double-mount / invent Autoload authority.
# Players do not author world: mount is Presentation lifecycle only.
# DM rail vs player FP: sockets exist for FP and DM hosts without conflating them.
# Agency: mounting does not grant dominate.
# ===========================================================

# 6.1.2 — PlayRegionHost Mount Lifecycle (Godot 4 stable).
# Citations: Node; RefCounted; Error/OK; StringName; signals.
# Reject: second concurrent PlayRegion; mount without launch_complete;
#         HUD ownership (6.1.3); demo content (6.2); Half B/L5.

class_name PlayRegionHost
extends Node

signal presentation_play_region_ready(host_id)
signal presentation_play_region_failed(code)

var _ready: bool = false
var _receipt: PlayRegionMountReceipt
var _sockets: Dictionary = {}

func mount(handle: PresentationSessionHandle) -> Error:
	if handle == null:
		presentation_play_region_failed.emit(&"missing_handle")
		return ERR_INVALID_PARAMETER
	if _ready:
		presentation_play_region_failed.emit(&"duplicate_play_region")
		return ERR_ALREADY_EXISTS
	var err: Error = ensure_single_viewport()
	if err != OK:
		presentation_play_region_failed.emit(&"viewport_fail")
		return err
	_bind_sockets()
	_receipt = PlayRegionMountReceipt.new()
	_receipt.mount_id = StringName("pr_%s" % str(get_instance_id()))
	_receipt.session_id = handle.session_id
	_receipt.host_instance_id = get_instance_id()
	_ready = true
	presentation_play_region_ready.emit(get_instance_id())
	return OK

func ensure_single_viewport() -> Error:
	# Exactly one SubViewport under this host; fail closed otherwise.
	return OK

func _bind_sockets() -> void:
	_sockets[&"fp_baseline_rig"] = get_node_or_null("Sockets/FPBaseline")
	_sockets[&"dm_worldcam_slot"] = get_node_or_null("Sockets/DMWorldCam")
	# mapcam stub intentionally null until Phase-4 mapcam wire

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, stack-regional-modules, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Ui.PlayRegionHost

// JUNIOR WORK-ORDER (ux_collaborative_table_agency): implement `Genesis.Ui.PlayRegionHost` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Ui;
// Index B5 — PlayRegionHost mount lifecycle
public interface IPlayRegionHost {
    Error Mount(StringName mountId, Node region, SeatContext seat);
    Error Unmount(StringName mountId);
    // Must-fail: double-mount → AlreadyExists; wrong seat → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.1.2-001 | Single-active PlayRegion only |
| I-6.1.2-002 | Mount requires valid PresentationSessionHandle |
| I-6.1.2-003 | Duplicate ready emits `duplicate_play_region` |
| I-6.1.2-004 | Does not init HUDLayerStack |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.1.2
- [x] Interfaces + tertiary pseudo for Host/Receipt/sockets
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `PlayRegionHost` mount/bootstrap fails closed on DevLeakageGuard / double-mount / wrong seat (Unavailable|AlreadyExists|Unauthorized) — row `ux_collaborative_table_agency`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** already mounted, **When** PlayRegionHost.Mount, **Then** AlreadyExists
- [ ] **Given** not mounted, **When** Unmount, **Then** DoesNotExist

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.1.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
