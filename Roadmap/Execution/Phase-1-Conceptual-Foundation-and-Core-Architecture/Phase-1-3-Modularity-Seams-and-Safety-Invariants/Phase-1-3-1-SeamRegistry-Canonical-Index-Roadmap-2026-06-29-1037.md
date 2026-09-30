---
title: Phase 1.3.1 — SeamRegistry Canonical Index (Execution)
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.3.1"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]]'
status: active
priority: high
progress: 55
handoff_readiness: 74
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
deepen_complete: true
paint_ux_catalog: true
paint_status: painted
paint_campaign_id: exec-ux-paint-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_world_generation
created: 2026-09-29
updated: 2026-09-29
tags:
- roadmap
- genesis-mythos-master
- phase-1
- seam-registry
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
weave_pass: exec-gap3-host-index-20260929
---

# Phase 1.3.1 — SeamRegistry Canonical Index (Execution)

**Junior-complete host index:** [[Docs/SeamRegistry-CSharp-Host-Index]] (methods, errors, seat/authority for SeamRegistry + critical Phase 1–5 hosts). This leaf owns seam vocabulary; the index owns cross-phase C# port contracts.
Execution tertiary: seam id vocabulary, four families, PortBinder, DRAFT→PUBLISHED→DEPRECATED. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — published seams **enable** Phase-2 WorldShell swaps without player mid-session inject.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Session-scoped replaceability catalog with completeness gates |
| Inspiration / L5 bar (advisory) | Table/DM can swap published ports; players do not bind mid-session; CompletenessGate before world commit |
| Inspiration (studied) | (1) Conceptual 1.3.1 + rollup. (2) Execution 1.3 SeamRegistry. (3) Execution 1.2.1 StageEdgeRegistry type names. |
| Execution mechanism | `SeamRegistry` + `PortBinder` + family seed rows from 1.2.1 / 1.1.3 |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Conceptual 1.3.1 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Seam enablement | PUBLISHED gen.stage.* = system-authored world ports; input.parser.player_lite seat-gated |
| `does_not_mandate` | player PortBinder mid-session; Autoload SeamRegistry; soft PUBLISH without CompletenessGate |
| Pin color keys | Foundation Cyan · Blue (Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Players do not author first world | `input.parser.player_lite` + seat | PortBinder session-only | IntentEnvelope |
| Table can shape (published seams) | `promote_to_published` / CompletenessGate | unpublished → ERR_UNAVAILABLE | seam_published |
| Deterministic living world | gen.stage.* type names fixed | neighbor_guarantee | StageEdgeRegistry |
| Every world-hitting change DM-retconnable | DRAFT before PUBLISHED | CompletenessGate before capture | registry_incomplete |
| Collaborative / Phase-2 swap | PortBinder.resolve | new binds rejected on DEPRECATED | port_bound |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SeamRegistry` | Index + lifecycle transitions |
| `PortBinder` | Wire concrete port impls at session compose time only |
| `RegistryPublisher` | Ingest 1.2.1 stage rows → generation family DRAFT/PUBLISHED |
| `CompletenessGate` | Block PUBLISHED until required seam ids present |

## Interfaces

```text
PortBinder (RefCounted):
  + bind(seam_id: StringName, port: RefCounted) -> Error
  + resolve(seam_id: StringName) -> RefCounted
  signals: port_bound(seam_id), bind_rejected(seam_id, reason)

RegistryPublisher (RefCounted):
  + ingest_stage_edges(edges: Array[Dictionary], registry: SeamRegistry) -> Error
  + ingest_layer_owners(layer_table: Dictionary, registry: SeamRegistry) -> Error
  + promote_to_published(registry: SeamRegistry, seam_id: StringName) -> Error
  + assert_published_complete(registry: SeamRegistry) -> Error

CompletenessGate (RefCounted):
  + required_seam_ids() -> PackedStringArray
  + check(registry: SeamRegistry) -> Error
```

### Seed seam vocabulary (authoritative ids)

| seam_id | family | port_owner | layer_owner |
|---------|--------|------------|-------------|
| `gen.stage.terrain` | GENERATION | StageExecutorPort | WorldState |
| `gen.stage.biomes` | GENERATION | StageExecutorPort | WorldState |
| `gen.stage.pois` | GENERATION | StageExecutorPort | WorldState |
| `gen.stage.entities` | GENERATION | StageExecutorPort | WorldState |
| `gen.stage.sim_bootstrap` | GENERATION | StageExecutorPort | Simulation |
| `rules.plugin.core` | RULES | RulePluginPort | Simulation |
| `bus.sub.sim_default` | BUS | BusSubscriptionPort | Simulation |
| `bus.sub.canon_default` | BUS | BusSubscriptionPort | WorldState |
| `input.parser.player_lite` | INPUT | IntentParserPort | InputIntent |

**Neighbor guarantees:** GENERATION preserves 1.2.1 `in_type`/`out_type`; RULES preserves hook schema; BUS preserves category names from 1.1; INPUT preserves IntentEnvelope shape + CanonCommitBoundary routing.

## Pseudo-code

```pseudo
# 1.3.1 — SeamRegistry canonical index (Godot 4 stable).
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# PortBinder binds ONLY at SessionComposer time — players do not bind mid-session.
# CompletenessGate MUST pass before gen.stage.* capture / dry-run / world commit.
# input.parser.player_lite routes through CanonCommitBoundary + seat (players do not author).
# Preserve 1.2.1 in_type/out_type on GENERATION seam swap (Phase-2 WorldShell).
# ===========================================================

class_name PortBinder
extends RefCounted

signal port_bound(seam_id)
signal bind_rejected(seam_id, reason)

var _ports: Dictionary = {}

func bind(seam_id: StringName, port: RefCounted) -> Error:
	# JUNIOR WORK-ORDER: session compose only — refuse late player inject
	if port == null:
		bind_rejected.emit(seam_id, "null_port")
		return ERR_INVALID_PARAMETER
	_ports[seam_id] = port
	port_bound.emit(seam_id)
	return OK

func resolve(seam_id: StringName) -> RefCounted:
	return _ports.get(seam_id, null)


class_name CompletenessGate
extends RefCounted

func required_seam_ids() -> PackedStringArray:
	return PackedStringArray([
		&"gen.stage.terrain", &"gen.stage.biomes", &"gen.stage.pois",
		&"gen.stage.entities", &"gen.stage.sim_bootstrap",
		&"rules.plugin.core", &"bus.sub.sim_default", &"bus.sub.canon_default",
		&"input.parser.player_lite",
	])

func check(registry: SeamRegistry) -> Error:
	# JUNIOR WORK-ORDER: block world-hitting path until all required PUBLISHED
	for sid in required_seam_ids():
		var err := registry.assert_published(sid)
		if err != OK:
			return err
	return OK


class_name RegistryPublisher
extends RefCounted

func ingest_stage_edges(edges: Array, registry: SeamRegistry) -> Error:
	for e in edges:
		var to_stage: String = str(e.get("to", ""))
		var seam_id := StringName("gen.stage.%s" % to_stage.to_lower())
		var entry := {
			"seam_id": seam_id,
			"family": SeamFamily.GENERATION,
			"port_owner": &"StageExecutorPort",
			"swap_contract": {
				"replaceable_unit": "IStageExecutor",
				"neighbor_guarantee": "%s→%s types fixed" % [e.get("in_type"), e.get("out_type")],
			},
			"lifecycle": SeamLifecycle.DRAFT,
			"layer_owner": &"WorldState" if to_stage != "sim_bootstrap" else &"Simulation",
		}
		var err := registry.publish(entry)
		if err != OK:
			return err
	return OK

func promote_to_published(registry: SeamRegistry, seam_id: StringName) -> Error:
	# JUNIOR WORK-ORDER: explicit DRAFT→PUBLISHED — table/DM promote, not silent
	var entry: Dictionary = registry.get(seam_id)
	if entry.is_empty():
		return ERR_DOES_NOT_EXIST
	entry = entry.duplicate(true)
	entry["lifecycle"] = SeamLifecycle.PUBLISHED
	return registry.publish(entry)

func assert_published_complete(registry: SeamRegistry) -> Error:
	return CompletenessGate.new().check(registry)

# === WEAVE C# / .NET — see [[Docs/SeamRegistry-CSharp-Host-Index]] §A (canonical methods/errors/seats) ===
# Do NOT leave PortBinder.Bind as silent Ok without seat check.
namespace Genesis.Seams;
// ISeamRegistry.Publish / AssertPublished / Get / Deprecate
// IPortBinder.Bind(seamId, port, seat) → Unauthorized if !seat.AllowsSessionCompose()
// CompletenessGate.Check → Unavailable on first missing PUBLISHED id
```

## Invariants

| ID | Rule |
|----|------|
| I-1.3.1-001 | Only SessionComposer / PortBinder may bind concrete ports |
| I-1.3.1-002 | PUBLISHED requires CompletenessGate for required ids |
| I-1.3.1-003 | Generation seam ids mirror StageId vocabulary from 1.2 |
| I-1.3.1-004 | Deprecated seams remain resolvable until session end; new binds rejected |
| I-1.3.1-005 | Cross-phase host contracts live in SeamRegistry-CSharp-Host-Index — leaves must not invent parallel empty Ok stubs |

## Acceptance

- [x] Nine required seam ids listed
- [x] PortBinder session-only
- [x] conceptual_counterpart → frozen 1.3.1
- [x] **UX Catalog paint** — L5 seats/guards as JUNIOR WORK-ORDER (gold pattern)
- [x] **Gap 3:** points at junior-complete [[Docs/SeamRegistry-CSharp-Host-Index]]

## Status

`deepen_complete: true` + **`paint_status: painted`** + Gap 3 host-index link (`exec-gap3-20260929`). Next: Gap 4 wire Horizon 6.2 to real 1–5 contracts.