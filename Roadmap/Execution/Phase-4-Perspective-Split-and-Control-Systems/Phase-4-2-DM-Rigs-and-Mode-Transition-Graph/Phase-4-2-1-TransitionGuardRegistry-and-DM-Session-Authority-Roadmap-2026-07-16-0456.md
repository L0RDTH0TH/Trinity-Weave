---
title: Phase 4.2.1 — TransitionGuardRegistry and DM Session Authority (Execution)
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_camera_control_envelopes
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
- transition-guards
- dm-session-authority
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_camera_control_envelopes/L5]]'
- '[[ux_camera_control_envelopes]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph-Roadmap-2026-06-26-1730]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.2.1 — TransitionGuardRegistry and DM Session Authority (Execution)

Execution tertiary: ordered **TransitionGuardRegistry** + **DM session authority** (freeze/veto/overwrite/attach/dominate). Tertiary: TransitionGuardRegistry + DM session authority. **No Half B.** L5/SERIES are **read-only advisory feedstock** — first-failing guards enable legal FP↔DM and inter-DM seats; never silent noop; players do not author world via failed transitions.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | First-failing guard stack for FP↔DM and inter-DM ([[conceptual 4.2.1]]) |
| Inspiration / L5 bar (advisory) | dm_session_authority for FP→DM; narrative_veto_clear for DM→FP; Sensorium not_dominate; first failing guard_id emitted |
| Inspiration (studied) | (1) Conceptual 4.2.1. (2) Execution 4.2 / 4.1.1 ModeEdgeGuardLite. (3) 3.1 DMPauseGate / 3.3 veto |
| L5 / package crosswalk | phase-aligned `[[ux_camera_control_envelopes]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted registry + predicate chain; emit `presentation.transition_blocked` |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_camera_control_envelopes` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_camera_control_envelopes/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.2.1 + rollup |
| `dispatch_scope` | Execution tertiary **4.2.1** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_camera_control_envelopes` |
| Label | Perspective and control envelopes can change and cleanly return |
| Seats | `player`, `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Perspective.TransitionGuardRegistry` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | players get free third-person orbit as default; soft camera without hard restore |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| guard chain | `TransitionGuardRegistry.AssertAll` | any guard fail → Busy/Unauthorized | blocked_reason |
| DM session authority | `GuardDMSessionAuthority` | player seat → Unauthorized | authority attestation |
| pause freeze | `GuardNotDMPauseFrozen` | pause → Busy | no mode switch |
| dominate active | `GuardNotDominateActive` | dominate without release → reject | hold prior mode |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.TransitionGuardRegistry` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Perspective.TransitionGuardRegistry` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `TransitionGuardRegistry` | Ordered evaluate; last_blocked_guard_id |
| `GuardDMSessionAuthority` | `dm_session_authority` for FP→DM |
| `GuardNotDMPauseFrozen` | `not_dmpause_frozen` when leaving observe under freeze |
| `GuardNarrativeVetoClear` | `narrative_veto_clear` on DM→FP |
| `GuardOverwritePatchCompatible` | `overwrite_patch_compatible` |
| `GuardAttachTargetValid` | `attach_target_valid` for SensoriumAttach |
| `GuardNotDominateActive` | `not_dominate_active` |

## Interfaces

```text
const GUARD_DM_SESSION_AUTHORITY := &"dm_session_authority"
const GUARD_NOT_DMPAUSE_FROZEN := &"not_dmpause_frozen"
const GUARD_NARRATIVE_VETO_CLEAR := &"narrative_veto_clear"
const GUARD_OVERWRITE_PATCH_COMPATIBLE := &"overwrite_patch_compatible"
const GUARD_ATTACH_TARGET_VALID := &"attach_target_valid"
const GUARD_NOT_DOMINATE_ACTIVE := &"not_dominate_active"

TransitionGuard (RefCounted):
  + guard_id() -> StringName
  + evaluate(from_mode: int, to_mode: int, ctx: Dictionary) -> Error

TransitionGuardRegistry (RefCounted):
  + register(guard: TransitionGuard) -> void
  + evaluate(from_mode: int, to_mode: int, ctx: Dictionary) -> Error
  + last_blocked_guard_id() -> StringName
  signals: transition_blocked(guard_id, from_mode, to_mode)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_camera_control_envelopes L5 — advisory) ===
# Seats: first-failing guard stack — never invent / silent-pass illegal edges.
# Players do not author world: failed transitions emit blocked; no WorldState write.
# DM rail vs player FP: FP→DM requires dm_session_authority; DM→FP needs veto clear.
# Agency: SensoriumAttach path requires not_dominate_active.
# ===========================================================

# 4.2.1 — TransitionGuardRegistry + DM session authority (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
# Reject: Map annotation (4.2.2); rail chrome (4.2.3); Camera3D ownership.

class_name TransitionGuardRegistry
extends RefCounted

signal transition_blocked(guard_id, from_mode, to_mode)

var _guards: Array = []  # TransitionGuard
var _last_blocked: StringName = &""

func last_blocked_guard_id() -> StringName:
	return _last_blocked

func register(guard: TransitionGuard) -> void:
	_guards.append(guard)

func seed_default_stack() -> void:
	# Order matches conceptual catalog — first failing wins.
	register(GuardDMSessionAuthority.new())
	register(GuardNotDMPauseFrozen.new())
	register(GuardNarrativeVetoClear.new())
	register(GuardOverwritePatchCompatible.new())
	register(GuardAttachTargetValid.new())
	register(GuardNotDominateActive.new())

func evaluate(from_mode: int, to_mode: int, ctx: Dictionary) -> Error:
	_last_blocked = &""
	for g in _guards:
		var err: Error = g.evaluate(from_mode, to_mode, ctx)
		if err != OK:
			_last_blocked = g.guard_id()
			transition_blocked.emit(_last_blocked, from_mode, to_mode)
			return err
	return OK

# Policy sketch (per guard):
# FP→DM: require dm_session_authority; inter-DM under freeze OK if observe RO.
# DM→FP: narrative_veto_clear + overwrite_patch_compatible.
# →SensoriumAttach: attach_target_valid + not_dominate_active.

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-perspective-camera, engine-godot-463-dotnet | Catalog: ux_camera_control_envelopes | Type: Genesis.Perspective.TransitionGuardRegistry

// JUNIOR WORK-ORDER (ux_camera_control_envelopes): implement `Genesis.Perspective.TransitionGuardRegistry` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Perspective;
public interface ITransitionGuardRegistry {
    Error AllowTransition(PerspectiveMode from, PerspectiveMode to, SeatContext seat);
    // Must-fail: unauthorized mode edge → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.2.1-001 | First failing guard stops evaluate; emit transition_blocked |
| I-4.2.1-002 | Inter-DM under DMPause freeze remains RO-compatible |
| I-4.2.1-003 | SensoriumAttach blocked when dominate active |
| I-4.2.1-004 | No silent noop — rail chrome must surface guard_id (4.2.3) |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-4-2 folder
- [x] Path-qualified conceptual_counterpart
- [x] Interfaces + pseudo for TransitionGuardRegistry
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `TransitionGuardRegistry` transition/guard refuses unauthorized edges with `Unauthorized` — row `ux_camera_control_envelopes`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** GuardNotDMPauseFrozen while paused, **When** AssertAll, **Then** Busy and blocked_reason surfaced
- [ ] **Given** player seat, **When** GuardDMSessionAuthority, **Then** Unauthorized
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **4.2.2**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
