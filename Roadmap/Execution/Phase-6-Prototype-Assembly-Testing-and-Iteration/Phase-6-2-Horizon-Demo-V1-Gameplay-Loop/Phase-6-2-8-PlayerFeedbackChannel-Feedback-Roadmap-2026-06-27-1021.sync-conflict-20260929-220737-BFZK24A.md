---
title: Phase 6.2.8 — PlayerFeedbackChannel Feedback (Execution)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.8"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-8-PlayerFeedbackChannel-Feedback-Roadmap-2026-06-27-1021]]'
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
- feedback
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5]]'
- '[[ux_collaborative_table_agency]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-8-PlayerFeedbackChannel-Feedback-Roadmap-2026-06-27-1021]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-7-OverwriteDemonstrationSlot-Overwrite-Demo-Roadmap-2026-06-27-1005]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-3-HUDLayerStack-and-Kinesthetic-Honesty-Checklist-Roadmap-2026-06-27-0507]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.2.8 — PlayerFeedbackChannel Feedback (Execution)

Execution tertiary: **PlayerFeedbackChannel** (beat 8) — after overwrite_* aggregate rule/overwrite precursors into HUD **Transient** toasts (+ optional chrome pulse) → `demo_loop_complete`. Closes DemoLoopOrchestrator. Parallel spine under `Execution/Phase-6-…/Phase-6-2-…/`. **No Half B.** L5/SERIES advisory — PlayerFeedbackChannel closes demo loop with honest seat messaging; no world-author via toasts.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Demo loop feedback + loop_complete ([[conceptual 6.2.8]]) |
| Inspiration / L5 bar (advisory) | Feedback channel; surface blocked/overwrite results; Presentation only |
| Inspiration (studied) | (1) Conceptual 6.2.8. (2) Execution 6.2.7 / 6.2.5. (3) HUDLayerStack Transient (6.1.3). (4) DemoLoopOrchestrator close |
| L5 / package crosswalk | phase-aligned `[[ux_collaborative_table_agency]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | Channel Node; toast compose; single loop_complete |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_collaborative_table_agency` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_collaborative_table_agency/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.2.8 |
| `dispatch_scope` | Execution tertiary **6.2.8** mint (FAST DFS) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_collaborative_table_agency` |
| Label | Collaborative table agency / shared session surfaces |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Demo.PlayerFeedbackChannel` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | single player owns all agency; silent seat spoof |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `feedback_channel` | `PlayerFeedbackChannel` → IUiHost / HUDLayerStack | DemoToast **forbidden** | toast receipt |
| `hud_honesty` | DevLeakageGuard on channel | leakage → Unavailable | honest message |
| no sim write | Presentation only | feedback ≠ WorldState | UI residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.PlayerFeedbackChannel` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.PlayerFeedbackChannel` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `PlayerFeedbackChannel` | awaiting_overwrite → composing → toasting → loop_complete \| blocked |
| `FeedbackPayloadComposer` | Merge overwrite + rule echo into toast text |
| `HUDTransientBridge` | Push Transient on HUDLayerStack (no new layers) |
| `LoopCompletePublisher` | _(removed)_ — `demo_loop_complete` owned solely by DemoLoopOrchestrator (6.2) |

## Interfaces

```text
PlayerFeedbackChannel (Node):
  + arm_after_overwrite(outcome: StringName, rule_echo: StringName) -> Error
  + publish_feedback() -> Error
  + is_loop_complete() -> bool
  + run_beat() -> Error  # DemoLoopOrchestrator dispatch
  signals: feedback_published(summary), demo_feedback_blocked(code)
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_collaborative_table_agency L5 — advisory) ===
# Seats: feedback surfaces FP and DM outcomes — refuse silent drop.
# Players do not author world: feedback is Presentation chrome only.
# DM rail vs player FP: messages distinguish which seat produced residue.
# Agency: loop_complete reports agency outcome — does not grant new dominate.
# ===========================================================

# 6.2.8 — PlayerFeedbackChannel (Godot 4 stable).
# Citations: Node; StringName; Dictionary; Error/OK; signals.
# Reject: new persistent HUD layers; KH factory sign-off; publish without
#         overwrite_*; Half B/L5.
# demo_loop_complete: OWNED by DemoLoopOrchestrator (6.2) — this channel never emits it.

class_name PlayerFeedbackChannel
extends Node

signal feedback_published(summary)
signal demo_feedback_blocked(code)

enum State { AWAITING_OVERWRITE, COMPOSING, TOASTING, LOOP_COMPLETE, BLOCKED }
var _state: State = State.AWAITING_OVERWRITE
var _ow: StringName = &""
var _rule: StringName = &""
var _done: bool = false

func arm_after_overwrite(outcome: StringName, rule_echo: StringName) -> Error:
	if outcome != &"applied" and outcome != &"vetoed":
		_block(&"bad_overwrite_outcome")
		return ERR_INVALID_PARAMETER
	_ow = outcome
	_rule = rule_echo
	_state = State.COMPOSING
	return OK

func run_beat() -> Error:
	return publish_feedback()

func publish_feedback() -> Error:
	if _state != State.COMPOSING:
		_block(&"bad_state")
		return ERR_UNAVAILABLE
	if _done:
		_block(&"already_complete")
		return ERR_ALREADY_EXISTS
	_state = State.TOASTING
	var summary: Dictionary = {"overwrite": _ow, "rule": _rule, "toast": "demo_feedback"}
	# HUDLayerStack.push_transient(summary) — existing Transient only
	_done = true
	_state = State.LOOP_COMPLETE
	feedback_published.emit(summary)
	# DemoLoopOrchestrator (6.2) emits the single demo_loop_complete after this beat returns OK
	return OK

func is_loop_complete() -> bool:
	return _state == State.LOOP_COMPLETE

func _block(code: StringName) -> void:
	_state = State.BLOCKED
	demo_feedback_blocked.emit(code)

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Demo.PlayerFeedbackChannel

namespace Genesis.Demo;
// GAP4: PlayerFeedbackChannel → IUiHost / HUDLayerStack (6.1.3) — not DemoToast fake type
public sealed partial class PlayerFeedbackChannel : Node {
    private IUiHost _ui = null!;
    public Error PublishFeedback(FeedbackPayload payload, SeatContext seat) {
        if (payload == null) return Error.InvalidParameter;
        return _ui.PushHudChannel(payload, seat); // kinesthetic honesty checklist
    }
}

```

## Invariants

| ID | Rule |
|----|------|
| I-6.2.8-001 | arm_after_overwrite requires overwrite_applied\|vetoed |
| I-6.2.8-002 | Transient toast only — no new HUD layers |
| I-6.2.8-003 | demo_loop_complete emitted exactly once (emitted by DemoLoopOrchestrator 6.2 only; this channel never re-emits) |
| I-6.2.8-004 | Closes DemoLoopOrchestrator beat chain |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine under Phase-6-2 folder
- [x] Path-qualified `conceptual_counterpart` → frozen 6.2.8
- [x] Interfaces + tertiary pseudo for PlayerFeedbackChannel
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `PlayerFeedbackChannel` wrong-seat → Unauthorized; demo stub_only must not satisfy `ICampaignCapableDoDGate` alone — row `ux_collaborative_table_agency`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** DemoToast type, **When** bind, **Then** reject — IUiHost / HUDLayerStack only
- [ ] **Given** DevLeakageGuard fail, **When** feedback emit, **Then** Unavailable

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **6.3**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
