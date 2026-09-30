---
title: Phase 6 — Prototype Assembly, Testing, and Iteration (Execution)
roadmap-level: primary
phase-number: 6
subphase-index: "6"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
status: active
deepen_complete: phase6_tree_complete
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_collaborative_table_agency
priority: high
progress: 85
handoff_readiness: 74
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-28
updated: 2026-09-29
tags:
- paint_ux_catalog
- pkg_world_shell
- roadmap
- genesis-mythos-master
- phase-6
- prototype
- presentation-shell
- horizon-demo
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5]]'
- '[[ux_collaborative_table_agency]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6 — Prototype Assembly, Testing, and Iteration (Execution)

Execution primary: four tracks — **6.1** factory presentation shell, **6.2** horizon demo proof loop, **6.3** dual-track boundary glue, **6.4** Reference Exemplar. **Phase 6 end-state = PMG Medium Fantasy Reference Exemplar as assembled campaign-capable prototype** (graybox OK) — not demo-only. Horizon (6.2) proves shell+loop; Exemplar (6.4) is the shippable campaign bar. Parallel spine under `Execution/Phase-6-…/`. **No Half B.** Seats: FP≠DM rail; no player world-author.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Assemble factory shell + demo proof + **Exemplar as assembled campaign-capable prototype** ([[conceptual Phase 6]] / PMG) |
| Inspiration / L5 bar (advisory) | Exemplar = campaign bar (assembled); demo = ~30 min proof; seats preserved end-to-end |
| Inspiration (studied) | (1) Conceptual Phase 6 + 6.1–6.4. (2) Execution 5.x RuleEffectBus. (3) Execution 4.1 PerspectiveEnvelope / PlayerFPRig. (4) Execution 1.1 PresentationShell / InputIntent |
| L5 / package crosswalk | phase-aligned `[[ux_collaborative_table_agency]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + primary pseudo for shell mount → demo orchestrator → dual-track firewall |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_collaborative_table_agency` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual Phase 6 + 6.1–6.4 |
| `dispatch_scope` | Execution primary **Phase 6** enrich + secondaries **6.1–6.3** (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 6.1 | Factory Phase 0 Presentation Shell | **minted** (+ 6.1.1–6.1.3) |
| 6.2 | Horizon Demo V1 Gameplay Loop | **minted** (6.2.1–6.2.8 **minted**) |
| 6.3 | Factory vs Demo Track Boundary Glue | **minted** |
| 6.4 | Reference Exemplar | **minted** |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_collaborative_table_agency` |
| Label | Collaborative table agency / shared session surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.HorizonDemoHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | single player owns all agency; silent seat spoof |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `shared_table_seat` | Session bootstrap + DualTrackBoundary | missing seat → degraded | SeatContext |
| `hud_honesty` | HUDLayerStack + DevLeakageGuard | leakage → Unavailable | honest HUD layers |
| `feedback_channel` | PlayerFeedbackChannel / IUiHost | stub_only Exemplar → InvalidParameter | feedback receipt |
| demo vs exemplar | TrackAuthorityRegistry | demo stubs must not satisfy 6.4 | track attestation |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoHost` |
| `stack-ci-gdunit4net` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility | Owner secondary |
|--------|----------------|-----------------|
| `PresentationShellManifest` | Factory spine launch contract | 6.1 |
| `LaunchFlowController` | Bootstrap + DevLeakageGuard | 6.1 |
| `PlayRegionHost` | Single viewport + mount sockets | 6.1 |
| `HUDLayerStack` | Base/Mode/Context/Transient layers | 6.1 |
| `HorizonDemoManifest` | Demo loop contract + stage ids | 6.2 |
| `DemoLoopOrchestrator` | Ordered 8-beat proof loop | 6.2 |
| `DualTrackBoundaryManifest` | Factory vs demo seam | 6.3 |
| `TrackAuthorityRegistry` | Authority ownership matrix | 6.3 |
| `BuildProfileSelector` | `horizon_demo_in_shell` default | 6.3 |
| `ReferenceExemplarManifest` | Medium Fantasy pack DoD | 6.4 |

## Interfaces

```text
# Imports (RO consumers)
PerspectiveEnvelope (RefCounted)       # 4.1
PlayerFPRig (RefCounted)               # 4.1
InputIntent (RefCounted)               # 1.1
RuleEffectBus (RefCounted)             # 5.1
ModeTransitionGraph (RefCounted)       # 4.2
SeamRegistry (RefCounted)              # 1.3
SimTickScheduler (RefCounted)          # 3.1 RO stub only

PresentationShellManifest (RefCounted):
  + shell_id: StringName
  + play_region_socket: StringName
  + hud_stack_id: StringName
  + to_dict() -> Dictionary

PlayRegionHost (Node):  # Presentation only — never Simulation authority
  + mount_demo(demo: HorizonDemoManifest) -> Error
  + unmount(reason: StringName) -> Error
  signals: presentation_play_region_ready(host_id)

HorizonDemoManifest (RefCounted):
  + demo_id: StringName
  + stage_ids: Array
  + max_sim_ticks_per_loop: int  # ≤1
  + to_dict() -> Dictionary

DualTrackBoundaryManifest (RefCounted):
  + profile: StringName  # horizon_demo_in_shell | factory_only | demo_only
  + factory_attestation_key: StringName
  + demo_attestation_key: StringName
  + to_dict() -> Dictionary
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: factory vs demo tracks refuse authority bleed (6.3).
# Players do not author world: demo stubs + Exemplar never invent silent WorldState.
# DM rail vs player FP: demo loop includes FP explore AND DM cam transition seats.
# Agency: overwrite demo is gated slot — not free dominate author.
# ===========================================================

# Phase 6 primary — Prototype assembly spine (Godot 4 stable).
# Citations: Node presentation host; RefCounted manifests; Error/OK; StringName; signals.
# Reject: Autoload shell as Simulation; second PlayRegionHost; demo writing CanonRegistry;
#         factory attestation ≡ demo_loop_complete; L5/Half B.

class_name PrototypeAssemblyDirector
extends RefCounted

var _shell: PresentationShellManifest
var _host: PlayRegionHost
var _boundary: DualTrackBoundaryManifest
var _demo: HorizonDemoManifest

func boot_factory_shell(flow: LaunchFlowController) -> Error:
	if flow == null:
		return ERR_INVALID_PARAMETER
	var err: Error = flow.run_with_dev_leakage_guard()
	if err != OK:
		return err
	_shell = flow.shell_manifest()
	_host = flow.play_region_host()
	return OK

func attach_horizon_demo(demo: HorizonDemoManifest, orch: DemoLoopOrchestrator) -> Error:
	if _host == null or demo == null:
		return ERR_INVALID_PARAMETER
	if demo.max_sim_ticks_per_loop > 1:
		return ERR_INVALID_PARAMETER
	var err: Error = _host.mount_demo(demo)
	if err != OK:
		return err
	_demo = demo
	return orch.bind_host(_host)

func assert_attestation_separation() -> bool:
	# Factory attestation must never equal demo_loop_complete
	return _boundary.factory_attestation_key != _boundary.demo_attestation_key

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, stack-ci-gdunit4net, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Demo.HorizonDemoHost

// JUNIOR WORK-ORDER (ux_collaborative_table_agency): implement `Genesis.Demo.HorizonDemoHost` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
// Host Index: prefer typed host below over empty ILeafContract
namespace Genesis.Demo;
// Index B5 — proof-loop host; may stub behavior but MUST type against B1–B4 hosts
public interface IHorizonDemoHost {
    Error RunBeat(StringName beatId, SeatContext seat);
    // Must-fail: wrong seat → Unauthorized; never counts as CampaignCapable alone
}

```

## Validation signals

| Signal | Meaning |
|--------|---------|
| `presentation_play_region_ready` | Shell host mountable |
| `demo_loop_complete` | Horizon demo finished one loop |
| `boundary_profile_selected` | Build profile locked |
| Missing DevLeakageGuard | LaunchFlowController fails closed |

## Rejects

- Second `PlayRegionHost` instance
- Sim stub >1 tick per demo loop
- Conflating factory attestation with demo completion
- Half B / L5 / REGISTRY-CI as conceptual blockers

## Junior acceptance / verify (weave)

- [ ] **Verify** `HorizonDemoHost` wrong-seat → Unauthorized; demo stub_only must not satisfy `ICampaignCapableDoDGate` alone — row `ux_collaborative_table_agency`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** DevLeakageGuard fail, **When** HUDLayerStack mount, **Then** Unavailable
- [ ] **Given** demo stub_only receipt on Exemplar path, **When** ICampaignCapableDoDGate.Validate, **Then** InvalidParameter

## Research integration

Prior Godot Node/SceneTree citations: [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]. No new Research Task this FAST wave.

## Next

Phase-6 execution subtree **complete on disk** (6.1–6.4). **End-state path:** 6.4 junior assembly checklist (steps 0–14) + CampaignCapableDoDGate receipts = assembled graybox Exemplar. Demo≠Exemplar. Cursor: post-purge hostile revalidate. **No Half B.**

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.1**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
