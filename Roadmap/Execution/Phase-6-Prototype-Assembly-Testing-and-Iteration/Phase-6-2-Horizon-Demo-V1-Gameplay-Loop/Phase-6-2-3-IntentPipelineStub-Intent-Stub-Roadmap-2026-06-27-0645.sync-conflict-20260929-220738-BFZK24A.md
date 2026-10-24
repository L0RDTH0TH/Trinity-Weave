---
title: Phase 6.2.3 — IntentPipelineStub Intent Stub (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]'
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
- horizon-demo
- intent-stub
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5]]'
- '[[ux_collaborative_table_agency]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-3-IntentPipelineStub-Intent-Stub-Roadmap-2026-06-27-0645]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.2.3 — IntentPipelineStub Intent Stub (Execution)

Execution tertiary: **IntentPipelineStub** (beat 3) — capture interact sample → emit `intent_demo_interact` on `input.*` + `demo_intent_labeled` on `session.*`. Prereq: 6.2.2 `demo_fp_active`. **No** CanonRegistry / IntentResolver touch. Consumers: **6.2.4**. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B.** L5/SERIES advisory — IntentPipelineStub proves FP intent path; refuses player world-author.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Demo intent stub after FP ([[conceptual 6.2.3]]) |
| Inspiration / L5 bar (advisory) | Demo intent path; observe seats refuse; FP intents only in this beat |
| Inspiration (studied) | (1) Conceptual 6.2.3. (2) Execution 6.2.2. (3) InputIntent / `input.*` (1.1). (4) PerspectiveEnvelope self (4.1) |
| L5 / package crosswalk | phase-aligned `[[ux_collaborative_table_agency]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Stub Node; label Dictionary; bus signals only |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_collaborative_table_agency` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2.3 |
| `dispatch_scope` | Execution tertiary **6.2.3** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_collaborative_table_agency` |
| Label | Collaborative table agency / shared session surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.IntentPipelineStub` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | single player owns all agency; silent seat spoof |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| intent stub | `IntentPipelineStub` → IntentEnvelope bus | DemoIntent **forbidden** | intent observed |
| parse | IInputIntentHost | invalid → InvalidParameter | reject audit |
| no world write | bus only | stub must not mutate WorldState | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-intent-lore-loop` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.IntentPipelineStub` |
| `stack-input-intent` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.IntentPipelineStub` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.IntentPipelineStub` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `IntentPipelineStub` | awaiting_fp → awaiting_interact → labeling → labeled \| blocked |
| `InteractSampleCapture` | One-shot interact from `input.*` |
| `DemoIntentLabeler` | Produce `intent_demo_interact` payload |
| `DMPauseGateListener` | Block labeling while paused |

## Interfaces

```text
IntentPipelineStub (Node):
  + arm_after_fp(session_id: StringName) -> Error
  + on_interact(sample: Dictionary) -> Error
  + last_intent() -> Dictionary
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: intent_demo_interact(payload), demo_intent_labeled(session_id), demo_intent_blocked(code)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: stub accepts FP intents — refuse observe/DM-author invent as success.
# Players do not author world: world-author intents → ERR_UNAUTHORIZED in demo stub.
# DM rail vs player FP: still FP beat; DM cam later.
# Agency: SELF-tagged intents only in this stub beat.
# ===========================================================

# 6.2.3 — IntentPipelineStub (Godot 4 stable).
# Citations: Node; Dictionary; StringName; Error/OK; signals.
# Reject: CanonRegistry/IntentResolver writes; labeling without fp_active;
#         Half B/L5.

class_name IntentPipelineStub
extends Node

signal intent_demo_interact(payload)
signal demo_intent_labeled(session_id)
signal demo_intent_blocked(code)

enum State { AWAITING_FP, AWAITING_INTERACT, LABELING, LABELED, BLOCKED }
var _state: State = State.AWAITING_FP
var _last: Dictionary = {}

var _armed_session: StringName = &""

func run_beat() -> Error:
	var err := arm_after_fp(_armed_session)
	if err != OK:
		return err
	# Demo stub interact sample — labels without Canon touch
	return on_interact({"session_id": _armed_session, "sample": &"demo_interact"})

func arm_after_fp(session_id: StringName) -> Error:
	if session_id == StringName():
		_block(&"missing_session")
		return ERR_INVALID_PARAMETER
	_state = State.AWAITING_INTERACT
	return OK

func on_interact(sample: Dictionary) -> Error:
	if _state != State.AWAITING_INTERACT:
		_block(&"bad_state")
		return ERR_UNAVAILABLE
	if _dm_paused():
		_block(&"dm_pause")
		return ERR_BUSY
	_state = State.LABELING
	_last = {"kind": &"intent.demo_interact", "sample": sample}
	# Emit on input.* / session.* buses — no canon touch.
	intent_demo_interact.emit(_last)
	demo_intent_labeled.emit(_last.get("session_id", &"demo"))
	_state = State.LABELED
	return OK

func _dm_paused() -> bool:
	return false

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	demo_intent_blocked.emit(code)

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-intent-lore-loop, stack-input-intent, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Demo.IntentPipelineStub

namespace Genesis.Demo;
// GAP4: IntentPipelineStub labels IntentEnvelope (1.2.2 / IInputIntentHost) — no parallel DemoIntent type;
// MUST NOT call CanonRegistry/IntentResolver (still stub: bus emit only)
public sealed partial class IntentPipelineStub : Node {
    public Error OnInteract(IntentEnvelope sample, SeatContext seat) {
        if (sample.ImpliesWorldAuthor()) return Error.Unauthorized;
        // Emit intent_demo_interact on input.* bus — IntentEnvelope shape from Phase 1.2.2
        return Error.Ok;
    }
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.3-001 | arm_after_fp requires demo_fp_active |
| I-6.2.3-002 | No CanonRegistry or IntentResolver mutation |
| I-6.2.3-003 | DMPauseGate blocks labeling |
| I-6.2.3-004 | demo_intent_labeled is the sole beat-3 exit signal |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.3
- [x] Interfaces + tertiary pseudo for IntentStub
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `IntentPipelineStub` wrong-seat → Unauthorized; demo stub_only must not satisfy `ICampaignCapableDoDGate` alone — row `ux_collaborative_table_agency`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** DemoIntent type, **When** bind, **Then** reject — IntentEnvelope / IInputIntentHost only
- [ ] **Given** stub path, **When** WorldState mutate attempted, **Then** reject

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.2.4**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
