---
title: Phase 3.3 — DM Overwrite vs Deliberate Re-Generation Policy (Execution)
roadmap-level: secondary
phase-number: 3
subphase-index: "3.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_world_authorship_modability
priority: high
progress: 50
handoff_readiness: 72
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-3
- dm-authority
- overwrite
- re-generation
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy/Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-2-Off-Screen-Faction-Tribe-Activity/Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[ux_world_authorship_modability]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_authorship_modability/L5]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 3.3 — DM Overwrite vs Deliberate Re-Generation Policy (Execution)

Execution secondary: classify DM live-patch vs deliberate re-generation. Owns **DMOverwriteClass**, **LiveOverwriteRegistry**, **StructuralChangeDetector**, **OverwritePatchLayer**, **ReGenerationIntentQueue**, **DMPauseGate**, **SpeculativeDeltaReconciler**, **NarrativeDeltaVetoPolicy**, **CanonConflictArbiter**, **ProvenanceEnvelope**, **RollbackWindow**. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — every world-hitting change is DM-retconnable; lasting provenance + speculative residue reconciliation **enable** living-world continuity under DM authority.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Live patch vs structural re-gen policy |
| Inspiration / L5 bar (advisory) | DM-retconnable pause/patch; lasting dm_authority provenance; speculative residue never silent-drop; structural → ReGenerationIntent (never invent live) |
| Inspiration (studied) | (1) Conceptual 3.3 + rollup. (2) Execution 3.1 / 3.2. (3) Phase-1.3 provenance |
| Execution mechanism | C# / .NET (Godot 4.6.3) interfaces + pseudo for classify → pause → patch or queue re-gen |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_authorship_modability` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_authorship_modability/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 3.3 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_authorship_modability` |
| Label | World authorship / deliberate re-generation boundaries |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Envelope enablement | Phase-true moments → `Genesis.World.IDmOverwriteHost` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | silent structural mutate without retcon; players author first world; unconstrained regen every frame |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `dm_overwrite_live` | `IDmOverwriteHost` + LiveOverwriteRegistry | player seat → Unauthorized | OverwritePatchLayer |
| `deliberate_regen` | `ReGenerationIntentQueue` | structural change without queue → reject | regen intent row |
| `seat_gate_author` | DMSessionAuthority + DMPauseGate | pause frozen → Busy | author seat attested |
| narrative veto | `NarrativeDeltaVetoPolicy` | veto → no WorldState commit | veto audit |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-dm-overwrites` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.IDmOverwriteHost` |
| `stack-world-gen-pipeline` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.IDmOverwriteHost` |
| `stack-persistence-snapshots` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.IDmOverwriteHost` |
| `engine-godot-463-dotnet` | see Tech-Stack-Manifest-v1 | implement via `Genesis.World.IDmOverwriteHost` |
| Engine | Godot **4.6.3 .NET** / .NET 8 | `project.godot` + C# under `5-Attachments/Code-Repos/genesis-mythos-alpha/` |
| CI (when verifying) | `stack-ci-gdunit4net` | gdUnit4Net tests for acceptance below |

## Module map

| Module | Responsibility |
|--------|----------------|
| `DMOverwriteClass` | live_patch / canon_touching_patch / structural_re_gen |
| `LiveOverwriteRegistry` | Allowlist mutable fields per class |
| `StructuralChangeDetector` | Escalate topology/seed edits to re-gen |
| `OverwritePatchLayer` | Ordered patch stack at WorldStateCommitter |
| `ReGenerationIntentQueue` | Deferred region/full-world jobs |
| `DMPauseGate` | Halt tick advance; queue speculative deltas |
| `SpeculativeDeltaReconciler` | Merge/veto speculative vs DM authority |
| `NarrativeDeltaVetoPolicy` | accept / retroactive_veto / trigger_re_gen / fork_thread |
| `CanonConflictArbiter` | Escalate to Phase-2.2 IntentResolver |
| `ProvenanceEnvelope` | dm_authority + audit fields (1.3) |
| `RollbackWindow` | Pop last N live patches within session |

## Interfaces

```text
enum OverwriteClass { LIVE_PATCH, CANON_TOUCHING_PATCH, STRUCTURAL_RE_GEN }

ReGenerationIntent (RefCounted):
  + intent_id: StringName
  + scope: StringName          # region | full_world
  + region_ids: PackedStringArray
  + cost_copy_key: StringName
  + confirmed: bool
  + to_dict() -> Dictionary

OverwritePatch (RefCounted):
  + patch_id: StringName
  + overwrite_class: int
  + fields: Dictionary
  + provenance: Dictionary     # must include dm_authority:true
  + to_dict() -> Dictionary

DMOverwriteClass (RefCounted):
  + classify(edit: Dictionary) -> int

LiveOverwriteRegistry (RefCounted):
  + allows(overwrite_class: int, field_path: String) -> bool

StructuralChangeDetector (RefCounted):
  + is_structural(edit: Dictionary) -> bool

OverwritePatchLayer (RefCounted):
  + push(patch: OverwritePatch) -> Error
  + apply_pending(committer: RefCounted) -> Error
  signals: patch_applied(patch_id)

ReGenerationIntentQueue (RefCounted):
  + enqueue(intent: ReGenerationIntent) -> Error
  + peek() -> ReGenerationIntent
  signals: re_gen_queued(intent_id)

DMPauseGate (RefCounted):
  + is_paused() -> bool
  + may_advance() -> bool   # == not is_paused(); 3.1 / 3.1.1 call before clock.advance
  + pause(reason: StringName) -> void
  + resume() -> void
  + queue_speculative(delta: Dictionary) -> void
  + drain_speculative() -> Array
  signals: sim_paused(reason), sim_resumed()

SpeculativeDeltaReconciler (RefCounted):
  + reconcile(dm_patches: Array, speculative: Array) -> Dictionary

NarrativeDeltaVetoPolicy (RefCounted):
  + decide(delta: Dictionary) -> StringName
  # accept | retroactive_veto | trigger_re_gen | fork_thread

CanonConflictArbiter (RefCounted):
  + arbitrate(edit: Dictionary, intent_resolver: RefCounted) -> Error

RollbackWindow (RefCounted):
  + push(patch_id: StringName) -> void
  + pop_last(n: int) -> Array

DMAuthorityController (RefCounted):
  + apply_dm_edit(edit: Dictionary) -> Dictionary
  signals: overwrite_applied(patch_id), re_gen_queued(intent_id)
```

## Pseudo-code

```pseudo
# 3.3 — DM overwrite vs deliberate re-generation (Godot 4 stable).
# Citations: RefCounted, Error/OK, signals, PackedStringArray.
#
# === JUNIOR WORK-ORDER (ux_world_authorship_modability L5 — advisory) ===
# DM-retconnable: every world-hitting edit pauses via DMPauseGate — players do not author.
# Lasting world: OverwritePatch MUST carry dm_authority:true provenance.
# Speculative residue: SpeculativeDeltaReconciler on resume — NEVER silent drop.
# Structural living world: topology/seed → ReGenerationIntentQueue — NEVER live invent WorldState.
# ===========================================================

class_name DMAuthorityController
extends RefCounted

signal overwrite_applied(patch_id)
signal re_gen_queued(intent_id)

var _classifier: DMOverwriteClass
var _registry: LiveOverwriteRegistry
var _structural: StructuralChangeDetector
var _patches: OverwritePatchLayer
var _regen_q: ReGenerationIntentQueue
var _pause: DMPauseGate
var _reconciler: SpeculativeDeltaReconciler
var _veto: NarrativeDeltaVetoPolicy
var _canon: CanonConflictArbiter
var _rollback: RollbackWindow
var _committer: RefCounted
var _intent_resolver: RefCounted   # Phase-2.2

func apply_dm_edit(edit: Dictionary) -> Dictionary:
	var cls: int = _classifier.classify(edit)
	if _structural.is_structural(edit) or cls == OverwriteClass.STRUCTURAL_RE_GEN:
		# JUNIOR WORK-ORDER: structural → queue re-gen; never live-invent topology
		_pause.pause(&"structural_re_gen")
		var intent := ReGenerationIntent.new()
		intent.intent_id = StringName(str(edit.get("intent_id", "regen")))
		intent.scope = StringName(str(edit.get("scope", "region")))
		intent.region_ids = edit.get("region_ids", PackedStringArray())
		intent.confirmed = bool(edit.get("confirmed", false))
		_regen_q.enqueue(intent)
		re_gen_queued.emit(intent.intent_id)
		return {"event": &"dm.re_gen_queued", "intent": intent.to_dict()}
	# JUNIOR WORK-ORDER: DM-retconnable hold before live patch
	if not _pause.is_paused():
		_pause.pause(&"live_overwrite_window")
	if cls == OverwriteClass.CANON_TOUCHING_PATCH:
		var aerr := _canon.arbitrate(edit, _intent_resolver)
		if aerr != OK:
			return {"event": &"dm.canon_blocked", "error": aerr}
	for field_path in edit.get("fields", {}).keys():
		if not _registry.allows(cls, str(field_path)):
			return {"event": &"dm.registry_reject", "field": field_path}
	var patch := OverwritePatch.new()
	patch.patch_id = StringName(str(edit.get("patch_id", "patch")))
	patch.overwrite_class = cls
	patch.fields = edit.get("fields", {})
	# JUNIOR WORK-ORDER: lasting world — dm_authority provenance required
	patch.provenance = {"dm_authority": true, "source": edit.get("source", "dm")}
	_patches.push(patch)
	# JUNIOR WORK-ORDER: speculative residue — reconcile, never silent drop
	var speculative: Array = _pause.drain_speculative()
	var merged: Dictionary = _reconciler.reconcile([patch.to_dict()], speculative)
	_patches.apply_pending(_committer)
	_rollback.push(patch.patch_id)
	overwrite_applied.emit(patch.patch_id)
	_pause.resume()
	return {"event": &"dm.overwrite_applied", "merged": merged, "patch": patch.to_dict()}

# Structural re-gen → Phase-2.1 DAG after DM confirms cost.

# === WEAVE C# / .NET (Godot 4.6.3) — ISimTickHost ===
# Manifest: stack-dm-overwrites, stack-world-gen-pipeline, stack-persistence-snapshots, engine-godot-463-dotnet | Catalog: ux_world_authorship_modability
namespace Genesis.Sim;

public interface ISimTickHost {
    Error Tick(double simTime, SimSnapshot snapshot);
}

public sealed partial class SimTickHost : Node, ISimTickHost {
    // JUNIOR WORK-ORDER (ux_world_authorship_modability): lasting residue; overflow deferred not dropped
    // ACCEPT: modules tick in order; VERIFY no Autoload god-object
    public Error Tick(double simTime, SimSnapshot snapshot) {
        foreach (var mod in _modules) mod.Tick(simTime, snapshot.ToDict());
        return Error.Ok;
    }
}

```

## Invariants

| ID | Rule |
|----|------|
| I-3.3-001 | Structural edits → ReGenerationIntentQueue — never live WorldState surgery |
| I-3.3-002 | Every OverwritePatch carries `dm_authority: true` provenance |
| I-3.3-003 | Resume must run SpeculativeDeltaReconciler — no silent speculative drop |
| I-3.3-004 | Canon-touching patches require CanonConflictArbiter before commit |
| I-3.3-005 | RollbackWindow only pops live patches within session bound |
| I-3.3-006 | **L5:** DM-retconnable pause + lasting provenance preserve living-world continuity |

## Acceptance

- [x] Parallel spine `Execution/Phase-3-…/Phase-3-3-…/`
- [x] Path-qualified `conceptual_counterpart` → frozen 3.3
- [x] Module map + interfaces + pseudo for DMAuthorityController / DMPauseGate
- [x] **UX Catalog paint** — L5 DM-retconnable / lasting / residue as JUNIOR WORK-ORDER (gold pattern)
- [ ] Half B / playable ladder later

## Junior acceptance / verify (weave)

- [ ] **Verify** `IDmOverwriteHost` beat/host wrong-seat → Unauthorized; stub behavior typed against Index hosts — row `ux_world_authorship_modability`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Given** player seat, **When** IDmOverwriteHost live overwrite, **Then** Unauthorized and OverwritePatchLayer unchanged
- [ ] **Given** structural change without ReGenerationIntentQueue entry, **When** apply, **Then** reject (Busy/InvalidParameter)
- [ ] **Verify** `ISimTickHost` / module interfaces; overflow/residue never silently truncated

## Research integration

- DMPauseGate is Simulation-layer RefCounted — Presentation never advances ticks while paused.
- [[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]

## Subphase next

1. Phase-3 paint tree **COMPLETE**. Next campaign cursor: **Phase-4 primary**.

## Status

`deepen_complete: true` + **`paint_status: woven`** (`exec-ux-paint-20260929`). Phase-3 paint complete. Next: **Phase-4 primary**.

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

> **Weave:** `exec-weave-stack-ux-20260929` — stack + phase-aligned UX + conceptual shape (manual).
