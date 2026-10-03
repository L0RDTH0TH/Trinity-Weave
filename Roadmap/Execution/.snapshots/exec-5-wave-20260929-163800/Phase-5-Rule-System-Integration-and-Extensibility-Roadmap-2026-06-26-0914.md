---
title: Phase 5 — Rule System Integration and Extensibility (Execution)
roadmap-level: primary
phase-number: 5
subphase-index: "5"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
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
- '[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
catalog_row_ids:
- ux_combat_play_surface
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
updated: 2026-09-29
weave_pass: exec-weave-stack-ux-20260929
ruleset_lock: pathfinder_pf2e_orc
---
# Phase 5 — Rule System Integration and Extensibility (Execution)

**Scaffold stub only** — structure + high-level primary mirror. No Half B code. No secondary/tertiary deepen on this pass.

## Scope

Execution-track mirror of conceptual primary [[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]. Own machine-facing contracts, interfaces, and handoff readiness here as deepen proceeds; do not rewrite the conceptual note.

## Behavior

Deferred. Point of truth for *what* the phase must mean remains the conceptual counterpart. This note will later hold *how* execution delivers that behavior (module map, interfaces, validation signals).

## Handoff

- `handoff_readiness: 50` (scaffold floor)
- Conceptual counterpart: [[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]
- Next: deepen this primary, then DFS secondaries under `Execution/Phase-5-Rule-System-Integration-and-Extensibility/` — not part of this scaffold pass

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_combat_play_surface` |
| Label | Combat/rules resolve by authored paths including non-win ends |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Rules.IRulesPluginHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | win-only ends; SRD 5.1 / D&D first-plugin lock (superseded); AGPL dice libs |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |
| `ruleset_lock` | **pathfinder_pf2e_orc** (CDR `rules-base-pathfinder-pf2e-orc-2026-09-29`) — host ruleset-agnostic; first plugin = PF2e/ORC; **not** SRD 5.1 / D&D |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `rule_check` | `Genesis.Rules.IRulesPluginHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `pf2e_orc_plugin` | `Genesis.Rules.IRulesPluginHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `non_win_ends` | `Genesis.Rules.IRulesPluginHost` / leaf modules | wrong seat / out of contract | lasting readable residue |
| `dice_behind_host` | `Genesis.Rules.IRulesPluginHost` / leaf modules | wrong seat / out of contract | lasting readable residue |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.IRulesPluginHost` |
| `stack-character-creation` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.IRulesPluginHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.IRulesPluginHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |


## Pseudo-code

```pseudo

# === WEAVE C# / .NET (Godot 4.6.3) — IRulesPluginHost + DiceRoller + PF2e/ORC ===
# Manifest: stack-rules-engine, stack-character-creation, engine-godot-463-dotnet | Catalog: ux_combat_play_surface

# PF2e/ORC: RulesetPluginId = "pathfinder_pf2e_orc"; content tables remint pending.
# Host remains ruleset-agnostic — do NOT hardcode SRD 5.1 / D&D strings as first plugin.

namespace Genesis.Rules;

public interface IDiceRoller {
    RollResult Roll(DiceExpression expr, RuleContextFrame frame);
}

public interface IRulesPluginHost {
    Error BindPlugin(RulesetPluginId id);
    System.Collections.Generic.IReadOnlyList<RuleCandidate> Evaluate(RuleContextFrame frame);
    RollResult Roll(DiceExpression expr, RuleContextFrame frame);
}

public sealed class RuleEngineCore : IRulesPluginHost {
    // JUNIOR WORK-ORDER (ux_combat_play_surface): pf2e_orc_plugin + rule_check
    // ACCEPT: default BindPlugin = pathfinder_pf2e_orc (NOT srd_5_1)
    // ACCEPT: observe-only frame cannot WorldState-write
    // VERIFY: Roll → IDiceRoller (skizzerz/DiceRoller MIT); no AGPL dice host
    private readonly IDiceRoller _dice;
    private RulesetPluginId _active = new("pathfinder_pf2e_orc");
    public RuleEngineCore(IDiceRoller dice) => _dice = dice;
    public Error BindPlugin(RulesetPluginId id) { _active = id; return Error.Ok; }
    public System.Collections.Generic.IReadOnlyList<RuleCandidate> Evaluate(RuleContextFrame frame)
        => System.Array.Empty<RuleCandidate>();
    public RollResult Roll(DiceExpression expr, RuleContextFrame frame) => _dice.Roll(expr, frame);
}

```

## Junior acceptance / verify (weave)

- [ ] **Given** seat context allowed for `ux_combat_play_surface`, **When** junior implements `Genesis.Rules.IRulesPluginHost`, **Then** wrong-seat calls return unauthorized / emit blocked — never silent OK
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_combat_play_surface` (not blanket `ux_world_generation` unless Phase-2 gold) and moment→module rows match L5 feedstock
- [ ] **Verify** demo/plugin binder uses **PF2e/ORC** (`pathfinder_pf2e_orc`); no SRD 5.1 / 5e-bits first-plugin lock
- [ ] **Verify** rolls go through `IDiceRoller` / `IRulesPluginHost.Roll` (DiceRoller MIT) — not AGPL dice libs

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
