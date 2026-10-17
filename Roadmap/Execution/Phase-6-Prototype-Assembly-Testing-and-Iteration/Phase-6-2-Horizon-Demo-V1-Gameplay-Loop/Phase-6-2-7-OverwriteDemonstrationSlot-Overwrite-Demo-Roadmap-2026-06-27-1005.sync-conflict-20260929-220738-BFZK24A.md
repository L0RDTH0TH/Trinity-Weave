---
title: Phase 6.2.7 — OverwriteDemonstrationSlot Overwrite Demo (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.7"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roadmap-2026-06-27-1005]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_world_authorship_modability
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
- overwrite
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_authorship_modability/L5]]'
- '[[ux_world_authorship_modability]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roadmap-2026-06-27-1005]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.2.7 — OverwriteDemonstrationSlot Overwrite Demo (Execution)

Execution tertiary: **OverwriteDemonstrationSlot** (beat 7) — after `demo_dm_cam_active`, build demo `live_patch` on `demo_shrine_mood` via **OverwritePatchLayer**, run **NarrativeDeltaVetoPolicy** → `demo_overwrite_applied` | `demo_overwrite_vetoed`. Consumers: **6.2.8**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B.** L5/SERIES advisory — one gated overwrite/veto demo; not free player world-author.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | One demo overwrite/veto after DM cam ([[conceptual 6.2.7]]) |
| Inspiration / L5 bar (advisory) | Gated overwrite demo; DM retcon/veto; players do not free-author |
| Inspiration (studied) | (1) Conceptual 6.2.7. (2) Execution 6.2.6. (3) DMOverwriteClass / veto nouns (3.3). (4) SpawnBootstrap facets (6.2.1) |
| L5 / package crosswalk | phase-aligned `[[ux_world_authorship_modability]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Slot Node; single live_patch; veto gate; session signals |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_authorship_modability` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_world_authorship_modability/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2.7 |
| `dispatch_scope` | Execution tertiary **6.2.7** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_authorship_modability` |
| Label | World authorship / deliberate re-generation boundaries |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.OverwriteDemonstrationSlot` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | silent structural mutate without retcon; players author first world; unconstrained regen every frame |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| overwrite demo | `OverwriteDemonstrationSlot` → IDmOverwriteHost | player → Unauthorized | patch layer |
| regen | ReGenerationIntentQueue | structural without queue → reject | intent row |
| DemoOverwrite | **forbidden** | real host only | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-dm-overwrites` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.OverwriteDemonstrationSlot` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.OverwriteDemonstrationSlot` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `OverwriteDemonstrationSlot` | dm_cam_active → build_patch → veto → applied \| vetoed \| blocked |
| `OverwritePatchLayer` | Apply live_patch to demo_shrine_mood facet |
| `NarrativeDeltaVetoPolicy` | Demo veto (no CanonRegistry write) |
| `OverwriteOutcomePublisher` | demo_overwrite_applied / demo_overwrite_vetoed |

## Interfaces

```text
OverwriteDemonstrationSlot (Node):
  + arm_after_dm_cam() -> Error
  + apply_demo_overwrite() -> Error
  + last_outcome() -> StringName
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: demo_overwrite_applied(patch_id), demo_overwrite_vetoed(reason), demo_overwrite_blocked(code)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: overwrite demo is DM-gated — refuse player free-author overwrite.
# Players do not author world: demo overwrite is single slotted proof with veto.
# DM rail vs player FP: runs after DM cam active; FP does not own this beat.
# Agency: gated dominate demo must release — never leave silent binding.
# ===========================================================

# 6.2.7 — OverwriteDemonstrationSlot (Godot 4 stable).
# Citations: Node; Dictionary; StringName; Error/OK; signals.
# Reject: ReGenerationIntentQueue; CanonRegistry writes; multi-patch;
#         apply without dm_cam_active; Half B/L5.

class_name OverwriteDemonstrationSlot
extends Node

signal demo_overwrite_applied(patch_id)
signal demo_overwrite_vetoed(reason)
signal demo_overwrite_blocked(code)

enum State { AWAITING_DM_CAM, BUILDING_PATCH, VETO_CHECK, APPLIED, VETOED, BLOCKED }
var _state: State = State.AWAITING_DM_CAM
var _patch: Dictionary = {}
var _outcome: StringName = &""
var _done: bool = false

func run_beat() -> Error:
	var err := arm_after_dm_cam()
	if err != OK:
		return err
	return apply_demo_overwrite()

func arm_after_dm_cam() -> Error:
	_state = State.BUILDING_PATCH
	_patch = {"target": &"demo_shrine_mood", "op": &"live_patch", "id": &"demo_ow_001"}
	return OK

func apply_demo_overwrite() -> Error:
	if _state != State.BUILDING_PATCH:
		_block(&"bad_state")
		return ERR_UNAVAILABLE
	if _done:
		_block(&"already_done")
		return ERR_ALREADY_EXISTS
	_state = State.VETO_CHECK
	if _veto(_patch):
		_outcome = &"vetoed"
		_state = State.VETOED
		_done = true
		demo_overwrite_vetoed.emit(&"narrative_delta")
		return OK
	# OverwritePatchLayer.apply(_patch) — demo facet only
	_outcome = &"applied"
	_state = State.APPLIED
	_done = true
	demo_overwrite_applied.emit(_patch["id"])
	return OK

func last_outcome() -> StringName:
	return _outcome

func _veto(patch: Dictionary) -> bool:
	return false

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	demo_overwrite_blocked.emit(code)

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-dm-overwrites, engine-godot-463-dotnet | Catalog: ux_world_authorship_modability | Type: Genesis.Demo.OverwriteDemonstrationSlot

namespace Genesis.Demo;
// GAP4: OverwriteDemonstrationSlot → IDmOverwriteHost / ReGenerationIntentQueue (3.3) — gated demo
public sealed partial class OverwriteDemonstrationSlot : Node {
    private IDmOverwriteHost _overwrite = null!; // Phase 3.3 real host
    public Error RunDemoOverwrite(SeatContext seat) {
        if (!seat.AllowsDmRail()) return Error.Unauthorized;
        return _overwrite.EnqueueDemoStructuralPreview(); // not free dominate; AgencyEnvelope veto applies (4.3)
    }
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.7-001 | arm_after_dm_cam requires demo_dm_cam_active |
| I-6.2.7-002 | Target facet is demo_shrine_mood only |
| I-6.2.7-003 | No CanonRegistry / ReGen queue on demo path |
| I-6.2.7-004 | Exactly one applied\|vetoed outcome unlocks beat 8 |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.7
- [x] Interfaces + tertiary pseudo for OverwriteDemonstrationSlot
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `OverwriteDemonstrationSlot` wrong-seat → Unauthorized; demo stub_only must not satisfy `ICampaignCapableDoDGate` alone — row `ux_world_authorship_modability`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player seat, **When** OverwriteDemonstrationSlot, **Then** Unauthorized
- [ ] **Given** DemoOverwrite type, **When** bind, **Then** reject — IDmOverwriteHost only

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.2.8**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
