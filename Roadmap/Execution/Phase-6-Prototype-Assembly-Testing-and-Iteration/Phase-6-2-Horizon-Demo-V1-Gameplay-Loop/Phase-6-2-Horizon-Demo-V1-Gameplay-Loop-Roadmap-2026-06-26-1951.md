---
title: Phase 6.2 — Horizon Demo V1 Gameplay Loop (Execution)
roadmap-level: secondary
phase-number: 6
subphase-index: "6.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
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
- horizon-demo
- gameplay-loop
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5]]'
- '[[ux_collaborative_table_agency]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.2 — Horizon Demo V1 Gameplay Loop (Execution)

> **Stock Godot FPS (mandatory before Code-Exhibit player/camera):** [[Godot-Implementation-Decision-Matrix]] + [[Godot-Stock-Patterns]] (+ [[PIN-stock_godot_fps]]). Beat 2 FP explore enables stock `CharacterBody3D` FPS (`res://player/Player.tscn`); beat 6 DM cam swaps `Camera3D.Current` + disables FPS. PerspectiveEnvelope / PlayerFPRig / `ICameraRig` = **selector, not mover**. Demo receipts ≠ walk+look Done (operator F5).

Execution secondary: **HorizonDemoManifest** + **DemoLoopOrchestrator** + eight beat stubs (spawn → FP → intent → sim ≤1 → rule check → DM cam → overwrite → feedback). Mounts into **6.1** PlayRegionHost. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B.** L5/SERIES advisory — horizon demo loop proves FP≠DM rail + gated agency without inventing extra beats.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | ~30 min horizon demo proof loop ([[conceptual 6.2]]) |
| Inspiration / L5 bar (advisory) | Spawn→FP→intent→sim→rule→DM cam→overwrite→feedback; seats preserved |
| Inspiration (studied) | (1) Conceptual 6.2 + 6.2.1–6.2.8. (2) Execution 6.1 PlayRegionHost. (3) 5.1 RuleEngineCore probe. (4) 4.1 PlayerFPRig / 4.2 ModeTransitionGraph |
| L5 / package crosswalk | phase-aligned `[[ux_collaborative_table_agency]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Orchestrator stages emit `demo.*` on session bus; stubs only |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_collaborative_table_agency` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2 |
| `dispatch_scope` | Execution secondary **6.2** mint (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 6.2.1 | SpawnBootstrapController | **minted** |
| 6.2.2 | FPExploreRigHost | **minted** |
| 6.2.3 | IntentPipelineStub | **minted** |
| 6.2.4 | SimTickStub | **minted** |
| 6.2.5 | RuleCheckProbe | **minted** |
| 6.2.6 | DMCamTransitionSlot | **minted** |
| 6.2.7 | OverwriteDemonstrationSlot | **minted** |
| 6.2.8 | PlayerFeedbackChannel | **minted** |

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
| `shared_table_seat` | SpawnBootstrap → PlayRegionHost + seat | missing seat → degraded | session boot |
| beat orchestration | `HorizonDemoLoop` wires typed hosts | fake Demo* ports forbidden | beat receipts |
| `hud_honesty` | HUDLayerStack via 6.2.8 | leakage → Unavailable | honest toast |
| `feedback_channel` | PlayerFeedbackChannel → IUiHost | stub_only on Exemplar path → InvalidParameter | feedback row |

## Real contract wiring (Gap 4 — proof-loop stubs, Phase 1–5 types)

Demo beats stay stubs for *orchestration proof*, but inject **real** hosts from [[Docs/SeamRegistry-CSharp-Host-Index]] — no parallel `Demo*` fake ports.

| Beat | Stub owner | Real contract host (phase) | Fake type **forbidden** |
|------|------------|----------------------------|-------------------------|
| 6.2.1 spawn | `SpawnBootstrapController` | `PlayRegionHost` (6.1) + `PlayerFPRig`/`ICameraRig` (4.1) | `DemoSpawnPort` |
| 6.2.2 FP | `FPExploreRigHost` | `ICameraRig` + `PerspectiveEnvelope` (4.1) | `DemoCamera` |
| 6.2.3 intent | `IntentPipelineStub` | `IntentEnvelope` / `IInputIntentHost` (1.2.2) — bus only | `DemoIntent` |
| 6.2.4 sim | `SimTickStub` | `ISimTickHost` (3.1) ≤1 Tick | `DemoSimClock` |
| 6.2.5 rules | `RuleCheckProbe` | `IRulesPluginHost` + `IDiceRoller` (5.1) PF1 | `DemoRuleEngine` |
| 6.2.6 DM cam | `DMCamTransitionSlot` | `ICameraRig` WorldCam (4.1.3) + ModeTransitionGraph (4.2) | `DemoDmCam` |
| 6.2.7 overwrite | `OverwriteDemonstrationSlot` | `IDmOverwriteHost` / ReGen (3.3) + AgencyEnvelope (4.3) | `DemoOverwrite` |
| 6.2.8 feedback | `PlayerFeedbackChannel` | `IUiHost` / HUDLayerStack (6.1.3) | `DemoToast` |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | `IUiHost` | 6.2.8 → HUDLayerStack |
| `stack-simulation-tick` | `ISimTickHost` | 6.2.4 → Phase 3.1 host |
| `stack-rules-engine` | `IRulesPluginHost` | 6.2.5 → Phase 5.1 |
| `stack-perspective-camera` | `ICameraRig` | 6.2.2 / 6.2.6 |
| `engine-godot-463-dotnet` | Godot 4.6.3 .NET | game repo C# |
| CI (when verifying) | `stack-ci-gdunit4net` | ≥1 happy + ≥1 refuse per beat |

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
  + bind_stage_owner(stage_id: StringName, owner: Node) -> Error
  + run_loop(manifest: HorizonDemoManifest) -> Error
  + current_stage() -> StringName
  signals: demo_stage_entered(stage_id), demo_loop_complete(demo_id)

# Tertiary beat owners (detail notes) — Node + run_beat dispatch contract:
SpawnBootstrapController (Node):
  + run_beat() -> Error
  + begin_spawn(receipt: PlayRegionMountReceipt, handle: RefCounted) -> Error
FPExploreRigHost (Node):
  + run_beat() -> Error
  + activate_after_spawn(fp_rig: Node, envelope: RefCounted) -> Error
IntentPipelineStub (Node):
  + run_beat() -> Error
  + arm_after_fp(session_id: StringName) -> Error
SimTickStub (Node):
  + run_beat() -> Error
  + arm_after_intent(intent: Dictionary) -> Error
  + commit_one_tick() -> Error  # hard cap 1 per loop
RuleCheckProbe (Node):
  + run_beat() -> Error
  + arm_after_tick(event_id: StringName, log_row: Dictionary) -> Error
DMCamTransitionSlot (Node):
  + run_beat() -> Error
  + arm_after_rule_check(outcome: StringName) -> Error
OverwriteDemonstrationSlot (Node):
  + run_beat() -> Error
  + arm_after_dm_cam() -> Error
PlayerFeedbackChannel (Node):
  + run_beat() -> Error
  + publish_feedback() -> Error
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: ordered demo beats — refuse skip/invent beyond 6.2.8.
# Players do not author world: stubs prove path; not full WorldState author.
# DM rail vs player FP: loop includes FP explore AND DM cam transition.
# Agency: overwrite demonstration is gated slot with veto — not free dominate.
# GAP4: beat owners hold real Phase 1–5 host types (SeamRegistry-CSharp-Host-Index) — stub behavior only.
# ===========================================================

# 6.2 — Horizon Demo V1 Gameplay Loop (Godot 4 stable).
# Citations: RefCounted; Node; Error/OK; StringName; signals.
# Reject: >1 sim tick/loop; factory attestation rewrite; CanonRegistry writes;
#         Half B/L5; mounting without PlayRegionHost.

class_name DemoLoopOrchestrator
extends RefCounted

signal demo_stage_entered(stage_id)
signal demo_loop_complete(demo_id)

var _host: PlayRegionHost
var _current_stage: StringName = &""
var _stage_owners: Dictionary = {}  # StringName -> Node beat owner (6.2.1–6.2.8)
var _stages: Array = [
	&"spawn", &"fp_explore", &"intent", &"sim",
	&"rule_check", &"dm_cam", &"overwrite", &"feedback"
]

func current_stage() -> StringName:
	return _current_stage

func bind_host(host: PlayRegionHost) -> Error:
	if host == null:
		return ERR_INVALID_PARAMETER
	_host = host
	return OK

func bind_stage_owner(stage_id: StringName, owner: Node) -> Error:
	if stage_id == &"" or owner == null or not owner.has_method("run_beat"):
		return ERR_INVALID_PARAMETER
	_stage_owners[stage_id] = owner
	return OK

func run_loop(manifest: HorizonDemoManifest) -> Error:
	if _host == null or manifest == null:
		return ERR_INVALID_PARAMETER
	if manifest.max_sim_ticks_per_loop > 1:
		return ERR_INVALID_PARAMETER
	for stage_id in _stages:
		_current_stage = stage_id
		emit_signal("demo_stage_entered", stage_id)
		var err: Error = _run_stage(stage_id)
		if err != OK:
			return err
	# Sole owner of demo_loop_complete (6.2). 6.2.8 never re-emits.
	emit_signal("demo_loop_complete", manifest.demo_id)
	return OK

func _run_stage(stage_id: StringName) -> Error:
	# Dispatch to tertiary beat owners — never silent OK without owner.
	var owner = _stage_owners.get(stage_id)
	if owner == null:
		return ERR_DOES_NOT_EXIST
	return owner.run_beat()

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, stack-simulation-tick, stack-rules-engine, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency
# GAP4: orchestrator dispatches stubs that hold Phase 1–5 host refs — see Real contract wiring table
# Index: [[Docs/SeamRegistry-CSharp-Host-Index]]

namespace Genesis.Demo;
public sealed class HorizonDemoLoop {
    // Injected real hosts (not parallel fakes):
    // PlayRegionHost, ICameraRig, ISimTickHost, IRulesPluginHost, IDmOverwriteHost, IUiHost
    public Error RunLoop(HorizonDemoManifest manifest, SeatContext seat) {
        if (!seat.AllowsSharedTable()) return Error.Unauthorized;
        // bind_stage_owner → each beat.run_beat() using real contract types above
        return Error.Ok;
    }
}

```

## Validation signals

| Signal | Meaning |
|--------|---------|
| `demo_stage_entered` | Beat started |
| `demo_loop_complete` | Full 8-beat pass |
| SimTickStub second call | ERR_BUG / reject |

## Rejects

- Demo owning factory attestation keys
- Sim >1 tick per loop
- Half B / L5

## Next

Phase-6 execution subtree **complete on disk** (6.1–6.4; 6.1.1–6.1.3; 6.2.1–6.2.8). Batch validate/IRA only. Cursor: `map_gen_complete` / `6.2.8`. **No Half B.** L5/SERIES advisory (see UX Catalog paint).

## Junior acceptance / verify (weave)

- [ ] **Verify** `HorizonDemoLoop` wrong-seat → Unauthorized; demo stub_only must not satisfy `ICampaignCapableDoDGate` alone — row `ux_collaborative_table_agency`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** beat wiring, **When** any Demo* fake port injected, **Then** reject — must bind Host Index B1–B4 types
- [ ] **Given** stub_only receipt used for Exemplar DoD, **When** validate, **Then** InvalidParameter

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.2.1**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
