---
title: Phase 6.2 — Horizon Demo V1 Gameplay Loop (Execution)
roadmap-level: secondary
phase-number: 6
subphase-index: "6.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
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
- horizon-demo
- gameplay-loop
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
catalog_row_ids:
- ux_collaborative_table_agency
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.2 — Horizon Demo V1 Gameplay Loop (Execution)

Execution secondary: **HorizonDemoManifest** + **DemoLoopOrchestrator** + eight beat stubs (spawn → FP → intent → sim ≤1 → rule check → DM cam → overwrite → feedback). Mounts into **6.1** PlayRegionHost. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | ~30 min horizon demo proof loop ([[conceptual 6.2]]) |
| Inspiration (studied) | (1) Conceptual 6.2 + 6.2.1–6.2.8. (2) Execution 6.1 PlayRegionHost. (3) 5.1 RuleEngineCore probe. (4) 4.1 PlayerFPRig / 4.2 ModeTransitionGraph |
| L5 / package crosswalk | _(n/a — no L5)_ |
| Execution mechanism | Orchestrator stages emit `demo.*` on session bus; stubs only |
| Validation signal | Secondary minted; tertiaries 6.2.1–6.2.8 pending DFS; nested V/IRA batch-later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | _(advisory)_ |
| `package_id` | _(Phase-6 TBD)_ |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2 |
| `dispatch_scope` | Execution secondary **6.2** mint (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 6.2.1 | SpawnBootstrapController | **pending** |
| 6.2.2 | FPExploreRigHost | **pending** |
| 6.2.3 | IntentPipelineStub | **pending** |
| 6.2.4 | SimTickStub | **pending** |
| 6.2.5 | RuleCheckProbe | **pending** |
| 6.2.6 | DMCamTransitionSlot | **pending** |
| 6.2.7 | OverwriteDemonstrationSlot | **pending** |
| 6.2.8 | PlayerFeedbackChannel | **pending** |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_collaborative_table_agency` |
| Label | Collaborative table agency / shared session surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.HorizonDemoLoop` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | single player owns all agency; silent seat spoof |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `shared_table_seat` | `Genesis.Demo.HorizonDemoLoop` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `hud_honesty` | `Genesis.Demo.HorizonDemoLoop` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `feedback_channel` | `Genesis.Demo.HorizonDemoLoop` / leaf modules | wrong seat / out of contract | lasting readable residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoLoop` |
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoLoop` |
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoLoop` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoLoop` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility | Owner tertiary |
|--------|----------------|----------------|
| `DemoLoopOrchestrator` | Ordered 8-beat runner | secondary |
| `SpawnBootstrapController` | Session spawn | 6.2.1 |
| `FPExploreRigHost` | FP explore mount | 6.2.2 |
| `IntentPipelineStub` | Intent stub | 6.2.3 |
| `SimTickStub` | ≤1 sim tick | 6.2.4 |
| `RuleCheckProbe` | RuleEngine evaluate probe | 6.2.5 |
| `DMCamTransitionSlot` | DM cam transition | 6.2.6 |
| `OverwriteDemonstrationSlot` | Overwrite demo | 6.2.7 |
| `PlayerFeedbackChannel` | Feedback channel | 6.2.8 |

## Interfaces

```text
DemoLoopOrchestrator (RefCounted):
  + bind_host(host: PlayRegionHost) -> Error
  + run_loop(manifest: HorizonDemoManifest) -> Error
  + current_stage() -> StringName
  signals: demo.stage_entered(stage_id), demo.loop_complete(demo_id)

SpawnBootstrapController (RefCounted):
  + bootstrap(session: PresentationSessionHandle) -> Error

FPExploreRigHost (Node):
  + attach(rig: PlayerFPRig) -> Error

IntentPipelineStub (RefCounted):
  + push(intent: InputIntent) -> Error

SimTickStub (RefCounted):
  + tick_once() -> Error  # hard cap 1 per loop

RuleCheckProbe (RefCounted):
  + probe(engine: RuleEngineCore, ctx: RuleContextFrame) -> Error
```

## Pseudo-code

```pseudo
# 6.2 — Horizon Demo V1 Gameplay Loop (Godot 4 stable).
# Citations: RefCounted; Node; Error/OK; StringName; signals.
# Reject: >1 sim tick/loop; factory attestation rewrite; CanonRegistry writes;
#         Half B/L5; mounting without PlayRegionHost.

class_name DemoLoopOrchestrator
extends RefCounted

signal demo_stage_entered(stage_id)
signal demo_loop_complete(demo_id)

var _host: PlayRegionHost
var _stages: Array = [
	&"spawn", &"fp_explore", &"intent", &"sim",
	&"rule_check", &"dm_cam", &"overwrite", &"feedback"
]

func bind_host(host: PlayRegionHost) -> Error:
	if host == null:
		return ERR_INVALID_PARAMETER
	_host = host
	return OK

func run_loop(manifest: HorizonDemoManifest) -> Error:
	if _host == null or manifest == null:
		return ERR_INVALID_PARAMETER
	if manifest.max_sim_ticks_per_loop > 1:
		return ERR_INVALID_PARAMETER
	for stage_id in _stages:
		emit_signal("demo_stage_entered", stage_id)
		var err: Error = _run_stage(stage_id)
		if err != OK:
			return err
	emit_signal("demo_loop_complete", manifest.demo_id)
	return OK

func _run_stage(stage_id: StringName) -> Error:
	# Tertiary owners implement; secondary only sequences.
	return OK

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, stack-simulation-tick, stack-rules-engine, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Demo.HorizonDemoLoop

namespace Genesis;
// JUNIOR WORK-ORDER (ux_collaborative_table_agency): implement `Genesis.Demo.HorizonDemoLoop` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
public interface ILeafContract { Error Execute(SeatContext seat); }

```

## Validation signals

| Signal | Meaning |
|--------|---------|
| `demo.stage_entered` | Beat started |
| `demo.loop_complete` | Full 8-beat pass |
| SimTickStub second call | ERR_BUG / reject |

## Rejects

- Demo owning factory attestation keys
- Sim >1 tick per loop
- Half B / L5

## Junior acceptance / verify (weave)

- [ ] **Given** seat context allowed for `ux_collaborative_table_agency`, **When** junior implements `Genesis.Demo.HorizonDemoLoop`, **Then** wrong-seat calls return unauthorized / emit blocked — never silent OK
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_collaborative_table_agency` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
