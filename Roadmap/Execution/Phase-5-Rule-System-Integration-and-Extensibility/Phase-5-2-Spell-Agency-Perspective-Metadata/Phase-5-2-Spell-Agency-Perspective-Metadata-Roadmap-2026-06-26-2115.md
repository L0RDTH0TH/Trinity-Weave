---
title: Phase 5.2 — Spell Agency and Perspective Metadata (Execution)
roadmap-level: secondary
phase-number: 5
subphase-index: "5.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata/Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_combat_play_surface
priority: high
progress: 70
handoff_readiness: 76
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- paint_ux_catalog
- pkg_world_shell
- roadmap
- genesis-mythos-master
- phase-5
- spell-metadata
- agency
- perspective
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_combat_play_surface/L5]]'
- '[[ux_combat_play_surface]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-2-Spell-Agency-Perspective-Metadata/Phase-5-2-Spell-Agency-Perspective-Metadata-Roadmap-2026-06-26-2115]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks/Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue/Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Player-FP-and-Perspective-Envelope/Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/PF1-Ruleset-Content-Scaffold]]'
weave_pass: exec-weave-stack-ux-20260929
ruleset_lock: pathfinder_pf1
---
# Phase 5.2 — Spell Agency and Perspective Metadata (Execution)

Execution secondary: **SpellAgencyPerspectiveManifest** + **SpellMetadataRegistry** + **DominateSpellBinding** + **VictimPassengerOverlayBinding** + **LiminalPresentationPolicy** + **AbsentProxyHintSpellBinding**. Routes via **RuleEffectBus** → **AgencyEnvelope** (4.3) / **PerspectiveEnvelope** (4.1). Victim overlay only. Parallel spine under `Execution/Phase-5-…/Phase-5-2-…/`. **No Half B.** L5/SERIES advisory — spell agency/perspective metadata binds seats. **Do not invent 5.2.2+ twins.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Spell → agency/perspective metadata ([[conceptual 5.2]]) |
| Inspiration / L5 bar (advisory) | Spell metadata binds agency seats; passenger_fp deferred; DM rail ≠ FP cast seats |
| Inspiration (studied) | (1) Conceptual 5.2. (2) Execution 5.1 EffectBus/Arbiter. (3) 4.3 AgencyEnvelope / PilotHandoff / AbsentProxy. (4) 4.1 PerspectiveEnvelope |
| L5 / package crosswalk | phase-aligned `[[ux_combat_play_surface]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + secondary pseudo for registry lookup → modify_agency / overlay |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_combat_play_surface` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_combat_play_surface/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 5.2 |
| `dispatch_scope` | Execution secondary **5.2** mint (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| 5.2.1 | _(invented — parent conceptual 5.2)_ SpellMetadataRegistry / Manifest | **minted** |
| 5.2.2+ | Dominate / overlay / liminal / proxy bindings | **skipped** — no conceptual tertiary twins under Roadmap/Phase-5-2-… (operator: do not invent) |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_combat_play_surface` |
| Label | Combat/rules resolve by authored paths including non-win ends |
| Seats | `shared_table`, `dm_as_player`, `player` |
| Envelope enablement | Phase-true moments → `Genesis.Rules.SpellMetadataRegistry` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | win-only ends; SRD 5.1 / D&D first-plugin lock (superseded); AGPL dice libs |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |
| `ruleset_lock` | **pathfinder_pf1** (CDR `rules-base-pathfinder-pf1-2026-09-29`) — host ruleset-agnostic; first plugin = PF1; **not** SRD 5.1 / D&D |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| spell lookup | `SpellMetadataRegistry` | unknown spell → DoesNotExist | overlay metadata |
| agency perspective | `SpellAgencyPerspectiveManifest` | dominate without binding → reject | victim/passenger overlay |
| liminal present | `LiminalPresentationPolicy` | Presentation ≠ CanonRegistry write | UX overlay only |
| rules dice | **delegate host** — not spell registry | registry ≠ IDiceRoller | — |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-rules-engine` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.SpellMetadataRegistry` |
| `stack-perspective-camera` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.SpellMetadataRegistry` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.Rules.SpellMetadataRegistry` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility | Owner |
|--------|----------------|-------|
| `SpellMetadataRegistry` | spell_id → agency/perspective metadata | 5.2.1 |
| `SpellAgencyPerspectiveManifest` | Declared effects + liminal flags | 5.2.1 |
| `SpellRulesetPlugin` | RulesetPlugin band 100–199 | 5.2.1 |
| `DominateSpellBinding` | Dominate / release via PilotHandoff | 5.2.2+ |
| `VictimPassengerOverlayBinding` | passenger_fp_overlay (victim only) | 5.2.2+ |
| `LiminalPresentationPolicy` | Liminal chrome while overlay active | 5.2.2+ |
| `AbsentProxyHintSpellBinding` | Hint → AbsentProxyPolicyTable (4.3.3) | 5.2.2+ |

## Interfaces

```text
SpellAgencyPerspectiveManifest (RefCounted):
  + spell_id: StringName
  + agency_ops: Array        # dominate | release | absent_proxy_hint
  + overlay: StringName      # none | passenger_fp_overlay
  + liminal: bool
  + priority: int            # within spell band 100–199
  + to_dict() -> Dictionary

SpellMetadataRegistry (RefCounted):
  + register(m: SpellAgencyPerspectiveManifest) -> Error
  + lookup(spell_id: StringName) -> SpellAgencyPerspectiveManifest
  + apply_to_frame(spell_id: StringName, ctx: RuleContextFrame) -> Error

DominateSpellBinding (RefCounted):
  + stage(target_id: StringName, handoff: PilotHandoffCoordinator) -> Error
  + release(reason: StringName, handoff: PilotHandoffCoordinator) -> Error

VictimPassengerOverlayBinding (RefCounted):
  + attach(victim_id: StringName, envelope: PerspectiveEnvelope) -> Error
  + detach(reason: StringName) -> Error
  # victim-only — never caster FOV hijack

LiminalPresentationPolicy (RefCounted):
  + chrome_for(overlay: StringName) -> Dictionary
  + allows_input(overlay: StringName, intent: InputIntent) -> bool
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_combat_play_surface L5 — advisory) ===
# Seats: spell perspective eligibility — refuse cast from illegal seats; no 5.2.2+ invent.
# Players do not author world: metadata alone never writes WorldState.
# DM rail vs player FP: spells tag FP vs DM-rail eligibility explicitly.
# Agency: spell agency tags consume P4 AgencyEnvelope — never invent dominate.
# ===========================================================

# 5.2 — Spell agency / perspective metadata secondary (Godot 4 stable).
# Citations: RefCounted; Error/OK; StringName; signals from RuleEffectBus.
# Reject: caster passenger_fp; dominate without PilotHandoff release; CanonRegistry writes;
#         quest band collision without Arbiter (defer_to_spell default).

class_name SpellRulesetPlugin
extends RefCounted  # implements RulesetPlugin

var _registry: SpellMetadataRegistry
var _handoff: PilotHandoffCoordinator
var _agency: AgencyEnvelope
var _perspective: PerspectiveEnvelope
var _overlay: VictimPassengerOverlayBinding
var _liminal: LiminalPresentationPolicy
var _proxy_hints: AbsentProxyHintSpellBinding

func collect(trigger: StringName, ctx: RuleContextFrame) -> Array:
	if trigger != &"spell_cast" and trigger != &"spell_release":
		return []
	var spell_id: StringName = ctx.spell_metadata.get("spell_id", &"")
	var m := _registry.lookup(spell_id)
	if m == null:
		return []
	var rule := RulePrimitive.new()
	rule.rule_id = StringName("spell." + str(spell_id))
	rule.band = 100
	rule.priority = m.priority
	rule.trigger = trigger
	rule.effect_set = [{"id": &"modify_agency", "payload": m.to_dict()}]
	return [rule]

func apply_effect(payload: Dictionary) -> Error:
	var ops: Array = payload.get("agency_ops", [])
	for op in ops:
		if op == &"dominate":
			var terr: StringName = payload.get("target_id", &"")
			var err := _handoff.stage_dominate(terr)
			if err != OK:
				return err
			err = _agency.set_agency(AgencyClass.ACTIVE_DOMINATE, terr, &"spell")
			if err != OK:
				return err
		elif op == &"release":
			var rerr := _handoff.release_dominate(&"spell_end")
			if rerr != OK:
				return rerr
		elif op == &"absent_proxy_hint":
			_proxy_hints.apply(payload, _agency)
	if payload.get("overlay", &"none") == &"passenger_fp_overlay":
		var vid: StringName = payload.get("victim_id", &"")
		var oerr := _overlay.attach(vid, _perspective)
		if oerr != OK:
			return oerr
		if payload.get("liminal", false):
			_liminal.chrome_for(&"passenger_fp_overlay")
	return OK

# Priority band 100–199; composes under RuleConflictArbiter with quest 200–299.

# === WEAVE C# / .NET (Godot 4.6.3) — IRulesPluginHost + DiceRoller + PF1 ===
# Manifest: stack-rules-engine, stack-perspective-camera, engine-godot-463-dotnet | Catalog: ux_combat_play_surface

# PF1: RulesetPluginId = "pathfinder_pf1"; vault F2 resolved → [[Docs/PF1-Ruleset-Content-Scaffold]] (BAB/saves L1–20 + spell slots + spell-list scaffold).
# Game-repo res://rules/pathfinder_pf1/ mint = Half B (not this leaf).
# see Junior-Tech-Adapt-How-To §3–4 · SeamRegistry-CSharp-Host-Index §B4
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
    // JUNIOR WORK-ORDER (ux_combat_play_surface): pf1_plugin + rule_check
    // ACCEPT: default BindPlugin = pathfinder_pf1 (NOT srd_5_1)
    // ACCEPT: observe-only frame cannot WorldState-write
    // VERIFY: Roll → IDiceRoller (skizzerz/DiceRoller MIT); no AGPL dice host
    private readonly IDiceRoller _dice;
    private RulesetPluginId _active = new("pathfinder_pf1");
    public RuleEngineCore(IDiceRoller dice) => _dice = dice;
    public Error BindPlugin(RulesetPluginId id) { _active = id; return Error.Ok; }
    public System.Collections.Generic.IReadOnlyList<RuleCandidate> Evaluate(RuleContextFrame frame)
        => System.Array.Empty<RuleCandidate>();
    public RollResult Roll(DiceExpression expr, RuleContextFrame frame) => _dice.Roll(expr, frame);
}

```

## Invariants

| ID | Rule |
|----|------|
| I-5.2-001 | passenger_fp_overlay attaches to **victim** only |
| I-5.2-002 | Dominate requires PilotHandoffCoordinator stage + release path |
| I-5.2-003 | SpellRulesetPlugin never writes CanonRegistry |
| I-5.2-004 | On spell vs quest conflict, Arbiter default `defer_to_spell` |

## Acceptance

- [x] UX Catalog paint DoD (`paint_status: woven`, JUNIOR WORK-ORDER, moment→module)
- [x] Parallel spine `Execution/Phase-5-…/Phase-5-2-…/`
- [x] Path-qualified conceptual counterpart
- [x] Module map + interfaces + secondary pseudo
- [ ] Nested Validator batch-later

## Junior acceptance / verify (weave)

- [ ] **Verify** `SpellMetadataRegistry` bind/evaluate/roll refuse paths emit Unauthorized/Unavailable (never silent OK); Roll→IDiceRoller when applicable — row `ux_combat_play_surface`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** unknown spell id, **When** SpellMetadataRegistry lookup, **Then** DoesNotExist
- [ ] **Given** dominate without DominateSpellBinding, **When** apply overlay, **Then** reject
- [ ] **Verify** demo/plugin binder uses **PF1** (`pathfinder_pf1`); no SRD 5.1 / 5e-bits first-plugin lock
- [ ] **Verify** rolls go through `IDiceRoller` / `IRulesPluginHost.Roll` (DiceRoller MIT) — not AGPL dice libs

## Subphase next

1. Execution tree complete on disk for this node.
2. Batch validate / residual IRA only — no further deepen. Cursor: `map_gen_complete` / `6.2.8`.

1. **5.2.2+** remain **skipped** — no conceptual tertiary twins; do not invent.

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Next paint: **5.2.1**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
