---
title: Phase 6.3 — Factory vs Demo Track Boundary Glue (Execution)
roadmap-level: secondary
phase-number: 6
subphase-index: "6.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue/Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roadmap-2026-06-26-2031]]'
status: active
priority: high
progress: 55
handoff_readiness: 72
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-6
- dual-track
- boundary-glue
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue/Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roadmap-2026-06-26-2031]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
---

# Phase 6.3 — Factory vs Demo Track Boundary Glue (Execution)

Execution secondary: **DualTrackBoundaryManifest** + **TrackAuthorityRegistry** + **MountContractGlue** + **AttestationSeparationPolicy** + **CrossTrackEventFirewall** + **FailureRoutingPolicy** + **BuildProfileSelector** (`horizon_demo_in_shell` default). Glue only — no demo beats. Parallel spine under `Execution/Phase-6-…/Phase-6-3-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Factory vs demo seam without authority bleed ([[conceptual 6.3]]) |
| Inspiration (studied) | (1) Conceptual 6.3. (2) Execution 6.1 / 6.2 manifests. (3) 1.3 SeamRegistry. (4) Phase-6 primary PrototypeAssemblyDirector |
| L5 / package crosswalk | deferred (no L5); active pins `pkg_world_shell` / `ux_world_generation` |
| Execution mechanism | RefCounted policies + event firewall on session bus |
| Validation signal | Secondary minted; no conceptual tertiaries under 6.3; nested V/IRA batch-later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | _(n/a)_ |
| `conceptual_pin` | Frozen conceptual 6.3 |
| `dispatch_scope` | Execution secondary **6.3** mint (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| _(none)_ | 6.3 has no conceptual tertiary tree | **n/a** — 6.4 + 6.1.x minted this wave; next **6.2.1** |

## Module map

| Module | Responsibility | Owner |
|--------|----------------|-------|
| `DualTrackBoundaryManifest` | Profile + attestation keys | 6.3 |
| `TrackAuthorityRegistry` | Who owns which socket/signal | 6.3 |
| `MountContractGlue` | Demo→PlayRegionHost mount rules | 6.3 |
| `AttestationSeparationPolicy` | Factory ≠ demo complete | 6.3 |
| `CrossTrackEventFirewall` | Drop illegal cross-track events | 6.3 |
| `FailureRoutingPolicy` | Fail closed per track | 6.3 |
| `BuildProfileSelector` | Default `horizon_demo_in_shell` | 6.3 |

## Interfaces

```text
enum BuildProfile { HORIZON_DEMO_IN_SHELL, FACTORY_ONLY, DEMO_ONLY }

TrackAuthorityRegistry (RefCounted):
  + owner_of(resource: StringName) -> StringName  # factory | demo | shared
  + assert_write(track: StringName, resource: StringName) -> Error

MountContractGlue (RefCounted):
  + validate_mount(host: PlayRegionHost, demo: HorizonDemoManifest) -> Error

AttestationSeparationPolicy (RefCounted):
  + keys_disjoint(m: DualTrackBoundaryManifest) -> bool

CrossTrackEventFirewall (RefCounted):
  + allow(event_id: StringName, from_track: StringName, to_track: StringName) -> bool

BuildProfileSelector (RefCounted):
  + select(profile: int) -> Error
  + current() -> int
  signals: boundary_profile_selected(profile)
```

## Pseudo-code

```pseudo
# 6.3 — Factory vs Demo Track Boundary Glue (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals.
# Reject: merging attestation keys; demo writing factory shell manifests;
#         silent cross-track events; Half B/L5.

class_name BuildProfileSelector
extends RefCounted

signal boundary_profile_selected(profile)

var _current: int = BuildProfile.HORIZON_DEMO_IN_SHELL
var _authority: TrackAuthorityRegistry
var _attest: AttestationSeparationPolicy
var _firewall: CrossTrackEventFirewall

func select(profile: int) -> Error:
	_current = profile
	emit_signal("boundary_profile_selected", profile)
	return OK

func gate_event(event_id: StringName, from_track: StringName, to_track: StringName) -> Error:
	if not _firewall.allow(event_id, from_track, to_track):
		return ERR_UNAUTHORIZED
	return OK

func validate_boundary(m: DualTrackBoundaryManifest) -> Error:
	if not _attest.keys_disjoint(m):
		return ERR_INVALID_PARAMETER
	return OK
```

## Validation signals

| Signal | Meaning |
|--------|---------|
| `boundary_profile_selected` | Profile locked |
| Attestation key collision | ERR_INVALID_PARAMETER |
| Firewall drop | ERR_UNAUTHORIZED |

## Rejects

- Factory attestation ≡ demo.loop_complete
- Demo mutating PresentationShellManifest
- Half B / L5

## Status

Phase-6 execution subtree **complete on disk** (6.1–6.4; 6.1.1–6.1.3; 6.2.1–6.2.8). Batch validate/IRA only. Cursor: `map_gen_complete` / `6.2.8`. No Half B. No L5.

> **Execution roll-up policy:** Status/AC on this note are the execution-track roll-up; no separate `*Roll-up*` mint on the Execution spine.

## Next

Phase-6 execution subtree **complete on disk** (6.1–6.4; 6.1.1–6.1.3; 6.2.1–6.2.8). Batch validate/IRA only. Cursor: `map_gen_complete` / `6.2.8`. No Half B. No L5.

