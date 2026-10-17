---
title: Phase 6 — Prototype Assembly, Testing, and Iteration (Execution)
roadmap-level: primary
phase-number: 6
subphase-index: "6"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
status: active
progress: 0
handoff_readiness: 50
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-28
tags:
- roadmap
- genesis-mythos-master
- phase
- execution
para-type: Project
links:
- '[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
catalog_row_ids:
- ux_collaborative_table_agency
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
updated: 2026-09-29
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6 — Prototype Assembly, Testing, and Iteration (Execution)

**Scaffold stub only** — structure + high-level primary mirror. No Half B code. No secondary/tertiary deepen on this pass.

## Scope

Execution-track mirror of conceptual primary [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]. Own machine-facing contracts, interfaces, and handoff readiness here as deepen proceeds; do not rewrite the conceptual note.

## Behavior

Deferred. Point of truth for *what* the phase must mean remains the conceptual counterpart. This note will later hold *how* execution delivers that behavior (module map, interfaces, validation signals).

## Handoff

- `handoff_readiness: 50` (scaffold floor)
- Conceptual counterpart: [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]
- Next: deepen this primary, then DFS secondaries under `Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/` — not part of this scaffold pass

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
| `shared_table_seat` | `Genesis.Demo.HorizonDemoHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `hud_honesty` | `Genesis.Demo.HorizonDemoHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `feedback_channel` | `Genesis.Demo.HorizonDemoHost` / leaf modules | wrong seat / out of contract | lasting readable residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoHost` |
| `stack-ci-gdunit4net` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Demo.HorizonDemoHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Pseudo-code

```pseudo

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, stack-ci-gdunit4net, engine-godot-463-dotnet | Catalog: ux_collaborative_table_agency | Type: Genesis.Demo.HorizonDemoHost

namespace Genesis;
// JUNIOR WORK-ORDER (ux_collaborative_table_agency): implement `Genesis.Demo.HorizonDemoHost` as C# on Godot 4.6.3 .NET
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// VERIFY: gdUnit4Net ≥1 happy + ≥1 refuse path
public interface ILeafContract { Error Execute(SeatContext seat); }

```

## Junior acceptance / verify (weave)

- [ ] **Given** seat context allowed for `ux_collaborative_table_agency`, **When** junior implements `Genesis.Demo.HorizonDemoHost`, **Then** wrong-seat calls return unauthorized / emit blocked — never silent OK
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_collaborative_table_agency` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
