---
title: Phase 4.3.3 — AgencyPersistenceLedger / AbsentProxy / RailStatePersistence (Execution)
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.3.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roadmap-2026-07-16-0749]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_agency_handoff_enter_exit
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
- agency-ledger
- absent-proxy
- rail-persist
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_agency_handoff_enter_exit/L5]]'
- '[[ux_agency_handoff_enter_exit]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roadmap-2026-07-16-0749]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-1-AgencyEnvelope-and-Active-Agency-Modes-Roadmap-2026-07-16-0709]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roadmap-2026-07-16-0729]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-DM-Rigs-and-Mode-Transition-Graph/Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 4.3.3 — AgencyPersistenceLedger / AbsentProxy / RailStatePersistence (Execution)

Execution tertiary: **AgencyPersistenceLedger** checkpoints; **AbsentProxyPolicyTable** proxy intents; **RailStatePersistence** DM rail cursor (session-local default). Tertiary: AgencyPersistenceLedger / AbsentProxy / RailStatePersistence. **No Half B.** L5/SERIES are **read-only advisory feedstock** — persist agency + proxy + rail; proxy intents never write WorldState; cross-load dominate requires checkpoint; DM-retconnable rail state session-local by default.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Persist agency + proxy + rail ([[conceptual 4.3.3]]) |
| Inspiration / L5 bar (advisory) | append-only ledger + save-slot checkpoints; AbsentProxy policy table immutable at runtime; proxy RO / 3.2 hints only; D-4.3-001/002/003 |
| Inspiration (studied) | (1) Conceptual 4.3.3 + D-4.3-001/002/003. (2) Execution 4.3.1/4.3.2. (3) 4.2.3 DMRailUXContract / 3.2 SinceYouLeft |
| L5 / package crosswalk | phase-aligned `[[ux_agency_handoff_enter_exit]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted ledger + policy table; Dictionary checkpoints per save-slot |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_agency_handoff_enter_exit` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_agency_handoff_enter_exit/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 4.3.3 + rollup |
| `dispatch_scope` | Execution tertiary **4.3.3** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_agency_handoff_enter_exit` |
| Label | Agency handoff enter/exit with clean return |
| Seats | `player`, `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.Agency.AgencyPersistenceLedger` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | permanent dominate without exit; Sensorium as pilot |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| persist rail | `AgencyPersistenceLedger.Upsert` | observe-only write → reject | ledger row |
| absent proxy | AbsentProxy record | missing ledger → Unconfigured | proxy id |
| restore | RailStatePersistence load | corrupt → InvalidParameter | restored rail |
| no invent | ledger ≠ CanonRegistry writer | canon invent → reject | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-persistence-snapshots` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.AgencyPersistenceLedger` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Agency.AgencyPersistenceLedger` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `AgencyPersistenceLedger` | Append-only session log + per-save-slot checkpoint |
| `AbsentProxyPolicyTable` | Static proxy rows + DM token for quest_steward |
| `RailStatePersistence` | Last rig_id / zoom band — session-local default |
| `SinceYouLeftHints` | RO consume 3.2 surfacing hints (no WorldState write) |

## Interfaces

```text
AbsentProxyPolicyRow (RefCounted):
  + proxy_policy_id: StringName
  + allowed_intents: PackedStringArray
  + surfacing_hint: StringName
  + max_duration_ticks: int

AbsentProxyPolicyTable (RefCounted):
  + row(policy_id: StringName) -> AbsentProxyPolicyRow
  + install(policy_id: StringName) -> Error
  + clear() -> void
  + active_policy_id() -> StringName

RailStatePersistence (RefCounted):
  + last_rig_id: StringName
  + zoom_band: int
  + export_enabled: bool
  + capture_from_rail(rail: DMRailUXContract) -> void
  + to_dict() -> Dictionary
  + restore(d: Dictionary) -> Error

AgencyPersistenceLedger (RefCounted):
  + append(event: Dictionary) -> Error
  + checkpoint(slot_id: StringName) -> Error
  + restore(slot_id: StringName) -> Error
  + last_events(n: int) -> Array
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_agency_handoff_enter_exit L5 — advisory) ===
# Seats: refuse runtime AbsentProxy matrix mutation (D-4.3-002).
# Players do not author world: proxy intents = Presentation RO + 3.2 hints only.
# DM rail vs player FP: RailStatePersistence session-local; export_enabled=false default.
# Agency: cross-load dominate requires checkpoint (D-4.3-003); ledger append-only.
# ===========================================================

# 4.3.3 — AgencyPersistenceLedger + AbsentProxy + RailState (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; Dictionary checkpoints.
# Reject: AgencyEnvelope classify (4.3.1); handoff SM (4.3.2); Camera3D;
#         mutating WorldState from proxy intents; runtime matrix mutation (D-4.3-002).

class_name AgencyPersistenceLedger
extends RefCounted

var _log: Array = []
var _slots: Dictionary = {}
var _proxy: AbsentProxyPolicyTable
var _rail: RailStatePersistence

func append(event: Dictionary) -> Error:
	event["ts_usec"] = Time.get_ticks_usec()
	_log.append(event)
	return OK

func checkpoint(slot_id: StringName) -> Error:
	# D-4.3-001: per-save-slot lean
	var snap := {
		"events_tail": _log.slice(maxi(_log.size() - 64, 0)),
		"proxy_policy_id": _proxy.active_policy_id(),
		"rail": _rail.to_dict() if _rail.export_enabled else {},
		"dominate_binding": event_last_binding()
	}
	_slots[slot_id] = snap
	return OK

func restore(slot_id: StringName) -> Error:
	# D-4.3-003: cross-load dominate requires checkpoint
	if not _slots.has(slot_id):
		return ERR_DOES_NOT_EXIST
	var snap: Dictionary = _slots[slot_id]
	var pid: StringName = snap.get("proxy_policy_id", &"")
	if pid != &"":
		var ierr := _proxy.install(pid)
		if ierr != OK:
			return ierr
	if _rail.export_enabled and snap.has("rail"):
		_rail.restore(snap["rail"])
	return OK

func seed_default_proxy_table() -> void:
	# D-4.3-002: static table; DM token only for proxy_quest_steward
	_proxy.register(&"proxy_idle_guard", ["patrol", "ambient_dialogue"], &"since_you_left_minor", 0)
	_proxy.register(&"proxy_quest_steward", ["quest_progress_local", "faction_ping"], &"since_you_left_major", 1200)
	_proxy.register(&"proxy_combat_stand_in", ["defensive_only"], &"combat_alert", 180)

# RailStatePersistence: default session-local; export_enabled=false.
# Proxy intents never write WorldState — Presentation RO + 3.2 hints only.

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-persistence-snapshots, engine-godot-463-dotnet | Catalog: ux_agency_handoff_enter_exit | Type: Genesis.Agency.AgencyPersistenceLedger

// JUNIOR WORK-ORDER (ux_agency_handoff_enter_exit): implement `Genesis.Agency.AgencyPersistenceLedger` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Agency;
public interface IAgencyPersistenceLedger {
    Error PersistRailState(RailState state, SeatContext seat);
    Error RestoreAbsentProxy(StringName entityId, SeatContext seat);
    // Must-fail: player write of DM rail state → Unauthorized
}

```

## Invariants

| ID | Rule |
|----|------|
| I-4.3.3-001 | Checkpoint scope = per-save-slot (D-4.3-001) |
| I-4.3.3-002 | AbsentProxyPolicyTable static; no runtime matrix mutation (D-4.3-002) |
| I-4.3.3-003 | Cross-load dominate requires ledger.restore (D-4.3-003) |
| I-4.3.3-004 | Proxy intents never mutate Simulation WorldState |
| I-4.3.3-005 | RailStatePersistence default session-local (`export_enabled=false`) |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-4-3 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 4.3.3
- [x] Interfaces + tertiary pseudo for ledger/proxy/rail
- [x] D-4.3-001/002/003 reflected in interfaces
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `AgencyPersistenceLedger` Assert/Handoff/Persist refuses wrong seat with `Unauthorized` and never silent OK — row `ux_agency_handoff_enter_exit`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** observe-only seat, **When** AgencyPersistenceLedger.Upsert, **Then** reject
- [ ] **Given** absent proxy without ledger row, **When** restore, **Then** Unconfigured
- [ ] **Verify** `ICameraRig` activate sets FOV/projection; players cannot bind WorldCam/MapCam; Sensorium RO (no intent transfer)

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **Phase-5 primary**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
