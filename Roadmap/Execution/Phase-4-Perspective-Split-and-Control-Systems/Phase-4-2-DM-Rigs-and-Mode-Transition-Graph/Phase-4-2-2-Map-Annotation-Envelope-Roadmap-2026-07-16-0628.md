---
title: Phase 4.2.2 — Map Annotation Envelope (Execution)
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-2-Map-Annotation-Envelope-Roadmap-2026-07-16-0628]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_dm_mapcam
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
- map-annotation
- mapcam
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_dm_mapcam/L5]]'
- '[[ux_dm_mapcam]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-2-Map-Annotation-Envelope-Roadmap-2026-07-16-0628]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-2-Off-Screen-Faction-Tribe-Activity/Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.2.2 — Map Annotation Envelope (Execution)

Execution tertiary: **MapAnnotationEnvelope** — Presentation-local pins/marks for MapCam; never WorldState. Tertiary: MapAnnotationEnvelope. **No Half B.** L5/SERIES are **read-only advisory feedstock** — session-local map marks bound to MapCam; canon-gate rejects sim-mutating marks; DM retconnable Presentation overlay — players do not author WorldState.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Session-local map annotations bound to MapCam ([[conceptual 4.2.2]]) |
| Inspiration / L5 bar (advisory) | map-annotation-local only; WorldState-implying intent → ERR_UNAUTHORIZED; DM retconnable marks; MapCam-bound visibility |
| Inspiration (studied) | (1) Conceptual 4.2.2. (2) Execution 4.1.3 MapCamFOV. (3) Phase-3.2 since-you-left overlays |
| L5 / package crosswalk | phase-aligned `[[ux_dm_mapcam]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted envelope + canon-gate reject for sim-mutating marks |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_dm_mapcam` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_dm_mapcam/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.2.2 + rollup |
| `dispatch_scope` | Execution tertiary **4.2.2** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_dm_mapcam` |
| Label | Map-fixed orthographic DM rail |
| Seats | `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Perspective.MapCamRig` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | MapCam is tilted WorldCam; players get MapCam |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `plane_locked` | MapCamPolicyBind + MapAnnotationEnvelope | tilt-as-WorldCam → InvalidParameter | ortho marks |
| `tokens_fog_los` | MapAnnotationMark overlays | player invent tokens → Unauthorized | overlay set |
| canon gate | `CanonGateReject` | invent-as-canon → reject | fact_rejected |
| since-you-left hints | SinceYouLeftOverlayHints | RO only — no WorldState write | hint overlay |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.MapCamRig` |
| `stack-vtt-overlays` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.MapCamRig` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.MapCamRig` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `MapAnnotationEnvelope` | Validate + store Presentation-local marks |
| `MapAnnotationMark` | Fields: anchor, layer_tag, visibility_band, session_ttl |
| `MapCamPolicyBind` | Active only when MapCam rig active |
| `CanonGateReject` | Reject sim-mutating mark intents (1.1) |
| `SinceYouLeftOverlayHints` | Consume 3.2 hints as RO overlays |

## Interfaces

```text
MapAnnotationMark (RefCounted):
  + mark_id: StringName
  + anchor: Vector3  # presentation space; not WorldState entity id authority
  + layer_tag: StringName
  + visibility_band: StringName
  + session_ttl_sec: float
  + to_dict() -> Dictionary

MapAnnotationEnvelope (RefCounted):
  + add_local(mark: MapAnnotationMark) -> Error
  + remove_local(mark_id: StringName) -> Error
  + clear_session() -> void
  + list_visible(band: StringName) -> Array
  + is_sim_mutating(mark: MapAnnotationMark) -> bool
  signals: annotation_changed(op, mark_id)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_dm_mapcam L5 — advisory) ===
# Seats: annotations only while MapCam / DM_MAP — refuse invent WorldState layers.
# Players do not author world: canon-gate rejects sim-mutating marks.
# DM rail vs player FP: marks are Presentation-local overlays on MapCam FOV.
# Agency: DM-retconnable; persistence of marks deferred to 4.3 if needed.
# ===========================================================

# 4.2.2 — MapAnnotationEnvelope (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; Vector3 presentation-local.
# Reject: WorldState writes; rail chrome (4.2.3); guard predicates (4.2.1);
#         Camera3D ownership; 4.3 persistence of marks.

class_name MapAnnotationEnvelope
extends RefCounted

signal annotation_changed(op, mark_id)

var _marks: Dictionary = {}  # StringName -> MapAnnotationMark
var _map_cam_active: bool = false

func set_map_cam_active(active: bool) -> void:
	_map_cam_active = active
	if not active:
		# session-local default: keep marks until clear_session / TTL
		pass

func is_sim_mutating(mark: MapAnnotationMark) -> bool:
	# Canon gate: any mark claiming world entity mutation / faction write
	if mark.layer_tag == &"worldstate_write":
		return true
	if mark.to_dict().get("mutates_sim", false):
		return true
	return false

func add_local(mark: MapAnnotationMark) -> Error:
	if not _map_cam_active:
		return ERR_UNAVAILABLE
	if is_sim_mutating(mark):
		return ERR_UNAUTHORIZED
	_marks[mark.mark_id] = mark
	annotation_changed.emit(&"add", mark.mark_id)
	return OK

func clear_session() -> void:
	_marks.clear()
	annotation_changed.emit(&"clear", &"")

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, stack-vtt-overlays, engine-godot-463-dotnet | Catalog: ux_dm_mapcam | Type: Genesis.Perspective.MapCamRig

// JUNIOR WORK-ORDER (ux_dm_mapcam): implement `Genesis.Perspective.MapCamRig` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Perspective;
// Index B3 — MapCam implements ICameraRig
public interface IMapCamRig : ICameraRig {
    Error SetOverlays(PackedStringArray flags, SeatContext seat);
    // Must-fail: player seat Activate on DM MapCam → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.2.2-001 | Annotations never write Simulation WorldState |
| I-4.2.2-002 | add_local requires MapCam active (or explicit bind) |
| I-4.2.2-003 | Sim-mutating marks → ERR_UNAUTHORIZED via canon gate |
| I-4.2.2-004 | Persistence / AgencyEnvelope handoff deferred to 4.3 |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-4-2 folder
- [x] Path-qualified conceptual_counterpart
- [x] Interfaces + pseudo for MapAnnotationEnvelope
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `MapCamRig.Activate(mode, seat)` returns `Error.Unauthorized` when seat mismatches rail (player on DM WorldCam/MapCam; never bare OK) — row `ux_dm_mapcam`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player invent tokens on map, **When** MapAnnotationMark write, **Then** Unauthorized
- [ ] **Given** invent-as-canon mark, **When** CanonGateReject, **Then** fact_rejected — no WorldState commit
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.2.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
