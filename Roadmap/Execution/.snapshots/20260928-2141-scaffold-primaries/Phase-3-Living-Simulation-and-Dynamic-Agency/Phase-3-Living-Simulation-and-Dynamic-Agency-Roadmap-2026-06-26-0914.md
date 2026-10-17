---
title: Phase 3 — Living Simulation and Dynamic Agency (Execution)
roadmap-level: primary
phase-number: 3
subphase-index: "3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
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
- '[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
catalog_row_ids:
- ux_living_world_continuity
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
updated: 2026-09-29
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 3 — Living Simulation and Dynamic Agency (Execution)

**Scaffold stub only** — structure + high-level primary mirror. No Half B code. No secondary/tertiary deepen on this pass.

## Scope

Execution-track mirror of conceptual primary [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]. Own machine-facing contracts, interfaces, and handoff readiness here as deepen proceeds; do not rewrite the conceptual note.

## Behavior

Deferred. Point of truth for *what* the phase must mean remains the conceptual counterpart. This note will later hold *how* execution delivers that behavior (module map, interfaces, validation signals).

## Handoff

- `handoff_readiness: 50` (scaffold floor)
- Conceptual counterpart: [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]
- Next: deepen this primary, then DFS secondaries under `Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/` — not part of this scaffold pass

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Sim.ISimTickHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_sim_weather_pulse` | `Genesis.Sim.ISimTickHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `ux_wa_faction_offscreen` | `Genesis.Sim.ISimTickHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `ux_wa_npc_agenda` | `Genesis.Sim.ISimTickHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `ux_canon_pipeline_feel` | `Genesis.Sim.ISimTickHost` / leaf modules | wrong seat / out of contract | lasting readable residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-simulation-tick` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.ISimTickHost` |
| `stack-weather-ambience` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.ISimTickHost` |
| `stack-npc-schedules` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.ISimTickHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Sim.ISimTickHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Pseudo-code

```pseudo

# === WEAVE C# / .NET (Godot 4.6.3) — ISimTickHost ===
# Manifest: stack-simulation-tick, stack-weather-ambience, stack-npc-schedules, engine-godot-463-dotnet | Catalog: ux_living_world_continuity
namespace Genesis.Sim;

public interface ISimTickHost {
    Error Tick(double simTime, SimSnapshot snapshot);
}

public sealed partial class SimTickHost : Node, ISimTickHost {
    // JUNIOR WORK-ORDER (ux_living_world_continuity): lasting residue; overflow deferred not dropped
    // ACCEPT: modules tick in order; VERIFY no Autoload god-object
    public Error Tick(double simTime, SimSnapshot snapshot) {
        foreach (var mod in _modules) mod.Tick(simTime, snapshot.ToDict());
        return Error.Ok;
    }
}

```

## Junior acceptance / verify (weave)

- [ ] **Given** seat context allowed for `ux_living_world_continuity`, **When** junior implements `Genesis.Sim.ISimTickHost`, **Then** wrong-seat calls return unauthorized / emit blocked — never silent OK
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_living_world_continuity` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
