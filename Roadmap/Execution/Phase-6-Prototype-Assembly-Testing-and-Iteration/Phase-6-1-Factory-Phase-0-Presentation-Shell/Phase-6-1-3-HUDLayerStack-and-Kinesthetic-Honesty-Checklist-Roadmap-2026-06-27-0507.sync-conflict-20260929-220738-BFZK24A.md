---
title: Phase 6.1.3 — HUDLayerStack and Kinesthetic Honesty Checklist (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]'
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
- hud
- kinesthetic-honesty
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5]]'
- '[[ux_collaborative_table_agency]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.1.3 — HUDLayerStack and Kinesthetic Honesty Checklist (Execution)

Execution tertiary: **HUDLayerStack** (Base/Mode/Context/Transient) + **KinestheticHonestyChecklist** KH-6.1-001..004 + `presentation_hud_active`. Prereq: 6.1.2 play_region_ready. Transient consumers → **6.2**. Closes **6.1** DFS. Parallel spine under `Execution/Phase-6-…/Phase-6-1-…/`. **No Half B.** L5/SERIES advisory — HUDLayerStack + KH checklist keep chrome honest; no player world-author via HUD.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | HUD layers + KH gates after PlayRegion ready ([[conceptual 6.1.3]]) |
| Inspiration / L5 bar (advisory) | HUD layers; KH gates; chrome surfaces blocked_reason; Presentation only |
| Inspiration (studied) | (1) Conceptual 6.1.3. (2) Execution 6.1 / 6.1.2. (3) PerspectiveEnvelope (4.1). (4) ModeTransitionGraph (4.2) RO reflect |
| L5 / package crosswalk | phase-aligned `[[ux_collaborative_table_agency]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | CanvasLayer stack + RefCounted KH checklist |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_collaborative_table_agency` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.1.3 |
| `dispatch_scope` | Execution tertiary **6.1.3** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_collaborative_table_agency` |
| Label | Collaborative table agency / shared session surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Ui.HudLayerStack` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | single player owns all agency; silent seat spoof |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `hud_honesty` | `HUDLayerStack.MountLayers` | DevLeakageGuard fail → Unavailable | layer ids |
| kinesthetic | KinestheticHonestyChecklist | fail checklist → Busy | checklist row |
| feedback | IUiHost toast path | Simulation write from HUD → reject | UI residue |
| shared_table | Presentation seat only | HUD ≠ WorldState | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.HudLayerStack` |
| `stack-vtt-overlays` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.HudLayerStack` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.HudLayerStack` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `HUDLayerStack` | Base / Mode / Context / Transient layers |
| `HUDLayerRegistry` | Layer id → CanvasLayer |
| `KinestheticHonestyChecklist` | KH-6.1-001..004 gates |
| `ModeChromeReflector` | RO bind to PerspectiveEnvelope |

## Interfaces

```text
KinestheticHonestyChecklist (RefCounted):
  + run_all(ctx: Dictionary) -> Error
  + last_fail_id() -> StringName  # KH-6.1-00N

HUDLayerRegistry (RefCounted):
  + register(layer_id: StringName, node: CanvasLayer) -> Error
  + get_layer(layer_id: StringName) -> CanvasLayer

HUDLayerStack (Node):
  + activate(receipt: PlayRegionMountReceipt, envelope: RefCounted) -> Error
  + registry() -> HUDLayerRegistry
  signals: presentation_hud_active(stack_id), presentation_hud_failed(code)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: HUD layers distinguish FP vs DM chrome — refuse conflate.
# Players do not author world: HUD is Presentation; KH gates honesty.
# DM rail vs player FP: DM badges/chrome do not grant WorldState author.
# Agency: kinesthetic honesty never equals dominate grant.
# ===========================================================

# 6.1.3 — HUDLayerStack / KinestheticHonestyChecklist (Godot 4 stable).
# Citations: Node; CanvasLayer; RefCounted; Error/OK; StringName; signals.
# Reject: HUD driving ModeTransitionGraph; activate without play_region_ready;
#         skipping KH gates; Half B/L5.

class_name HUDLayerStack
extends Node

signal presentation_hud_active(stack_id)
signal presentation_hud_failed(code)

var _registry: HUDLayerRegistry
var _kh: KinestheticHonestyChecklist
var _active: bool = false

func activate(receipt: PlayRegionMountReceipt, envelope: RefCounted) -> Error:
	if receipt == null:
		presentation_hud_failed.emit(&"missing_receipt")
		return ERR_INVALID_PARAMETER
	var err: Error = _kh.run_all({"receipt": receipt, "envelope": envelope})
	if err != OK:
		presentation_hud_failed.emit(_kh.last_fail_id())
		return err
	_ensure_layers()
	_reflect_mode(envelope)
	_active = true
	presentation_hud_active.emit(StringName(str(get_instance_id())))
	return OK

func _ensure_layers() -> void:
	for lid in [&"base", &"mode", &"context", &"transient"]:
		_registry.register(lid, get_node("Layers/%s" % String(lid)))

func _reflect_mode(envelope: RefCounted) -> void:
	# RO: Mode chrome mirrors PerspectiveEnvelope; never owns ModeTransitionGraph.
	pass

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, stack-vtt-overlays, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Ui.HudLayerStack

// JUNIOR WORK-ORDER (ux_collaborative_table_agency): implement `Genesis.Ui.HudLayerStack` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Ui;
// Index B5 — IUiHost / HUDLayerStack
public interface IHudLayerStack {
    Error MountLayer(StringName layerId, Control layer, SeatContext seat);
    Error UnmountLayer(StringName layerId);
    // Must-fail: DevLeakageGuard fail → Unavailable; wrong seat → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.1.3-001 | KH-6.1-001..004 must pass before hud_active |
| I-6.1.3-002 | Mode chrome is RO reflect — not ModeTransitionGraph owner |
| I-6.1.3-003 | activate requires PlayRegionMountReceipt |
| I-6.1.3-004 | Transient layer is the only 6.2 consumer surface |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-1 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.1.3
- [x] Interfaces + tertiary pseudo for HUD/KH
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `HudLayerStack` mount/bootstrap fails closed on DevLeakageGuard / double-mount / wrong seat (Unavailable|AlreadyExists|Unauthorized) — row `ux_collaborative_table_agency`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** DevLeakageGuard fail, **When** HUDLayerStack.MountLayers, **Then** Unavailable
- [ ] **Given** HUD attempts WorldState write, **When** channel, **Then** reject

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
