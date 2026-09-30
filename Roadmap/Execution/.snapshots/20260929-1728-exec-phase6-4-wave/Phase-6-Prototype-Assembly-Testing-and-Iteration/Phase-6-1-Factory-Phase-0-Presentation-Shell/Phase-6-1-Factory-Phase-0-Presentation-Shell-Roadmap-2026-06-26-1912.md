---
title: Phase 6.1 — Factory Phase 0 Presentation Shell (Execution)
roadmap-level: secondary
phase-number: 6
subphase-index: "6.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
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
- factory
- presentation-shell
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1405]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
catalog_row_ids:
- ux_collaborative_table_agency
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.1 — Factory Phase 0 Presentation Shell (Execution)

Execution secondary: **PresentationShellManifest** + **LaunchFlowController** + **DevLeakageGuard** + **PlayRegionHost** + **HUDLayerStack** + **KinestheticHonestyChecklist**. Factory spine only — not 6.2 demo. Parallel spine under `Execution/Phase-6-…/Phase-6-1-…/`. **No Half B. No L5.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Launch → PlayRegion → HUD factory shell ([[conceptual 6.1]]) |
| Inspiration (studied) | (1) Conceptual 6.1 + 6.1.1–6.1.3. (2) Execution Phase-6 primary. (3) 1.1 Presentation / InputIntent. (4) 4.1 PerspectiveEnvelope (RO mode reflect) |
| L5 / package crosswalk | _(n/a — no L5)_ |
| Execution mechanism | Node host + RefCounted controllers; KH checklist gates |
| Validation signal | Secondary minted; tertiaries 6.1.1–6.1.3 pending DFS; nested V/IRA batch-later |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | _(advisory — ui_presentation_shell)_ |
| `package_id` | _(Phase-6 TBD)_ |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.1 |
| `dispatch_scope` | Execution secondary **6.1** mint (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 6.1.1 | Launch Flow / DevLeakageGuard Session Bootstrap | **pending** |
| 6.1.2 | PlayRegionHost Mount Lifecycle | **pending** |
| 6.1.3 | HUDLayerStack / Kinesthetic Honesty Checklist | **pending** |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_collaborative_table_agency` |
| Label | Collaborative table agency / shared session surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Ui.IUiHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | single player owns all agency; silent seat spoof |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `shared_table_seat` | `Genesis.Ui.IUiHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `hud_honesty` | `Genesis.Ui.IUiHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `feedback_channel` | `Genesis.Ui.IUiHost` / leaf modules | wrong seat / out of contract | lasting readable residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.IUiHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Ui.IUiHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Module map

| Module | Responsibility | Owner tertiary |
|--------|----------------|----------------|
| `LaunchFlowController` | Bootstrap + DevLeakageGuard → PresentationSessionHandle | 6.1.1 |
| `DevLeakageGuard` | Fail-closed on leak paths | 6.1.1 |
| `PlayRegionHost` | Single viewport + sockets | 6.1.2 |
| `HUDLayerStack` | Base/Mode/Context/Transient | 6.1.3 |
| `KinestheticHonestyChecklist` | KH-6.1-001–004 gates | 6.1.3 |

## Interfaces

```text
PresentationSessionHandle (RefCounted):
  + session_id: StringName
  + shell_id: StringName
  + to_dict() -> Dictionary

LaunchFlowController (RefCounted):
  + run_with_dev_leakage_guard() -> Error
  + shell_manifest() -> PresentationShellManifest
  + play_region_host() -> PlayRegionHost
  + session_handle() -> PresentationSessionHandle

DevLeakageGuard (RefCounted):
  + check(paths: Array) -> Error
  + is_clean() -> bool

PlayRegionHost (Node):
  + ensure_single_viewport() -> Error
  + bind_socket(name: StringName, node: Node) -> Error
  + mount_demo(demo: HorizonDemoManifest) -> Error
  signals: presentation.play_region_ready(host_id)

HUDLayerStack (Node):
  + set_layer(layer: StringName, visible: bool) -> Error
  + reflect_mode(mode: int) -> Error  # RO from PerspectiveEnvelope — never drives ModeTransitionGraph
```

## Pseudo-code

```pseudo
# 6.1 — Factory Phase 0 Presentation Shell (Godot 4 stable).
# Citations: Node; Viewport; Error/OK; StringName; signals.
# Reject: driving ModeTransitionGraph from HUD; second PlayRegionHost;
#         Simulation Autoload; 6.2 demo beats inside factory attestation.

class_name LaunchFlowController
extends RefCounted

var _guard: DevLeakageGuard
var _shell: PresentationShellManifest
var _host: PlayRegionHost
var _handle: PresentationSessionHandle

func run_with_dev_leakage_guard() -> Error:
	var err: Error = _guard.check(_shell.leak_scan_paths())
	if err != OK:
		return err
	err = _host.ensure_single_viewport()
	if err != OK:
		return err
	_handle = PresentationSessionHandle.new()
	_handle.session_id = StringName(str(Time.get_ticks_msec()))
	_handle.shell_id = _shell.shell_id
	_host.emit_signal("presentation.play_region_ready", _host.get_instance_id())
	return OK

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Ui.IUiHost

namespace Genesis;
// JUNIOR WORK-ORDER (ux_collaborative_table_agency): implement `Genesis.Ui.IUiHost` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
public interface ILeafContract { Error Execute(SeatContext seat); }

```

## Validation signals

| Signal | Meaning |
|--------|---------|
| `presentation.play_region_ready` | Host ready for 6.2 mount |
| DevLeakageGuard fail | Launch aborted |
| Duplicate viewport | `ensure_single_viewport` → ERR |

## Rejects

- HUD driving ModeTransitionGraph
- Factory attestation requiring demo.loop_complete
- Half B / L5

## Junior acceptance / verify (weave)

- [ ] **Given** seat context allowed for `ux_collaborative_table_agency`, **When** junior implements `Genesis.Ui.IUiHost`, **Then** wrong-seat calls return unauthorized / emit blocked — never silent OK
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_collaborative_table_agency` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
