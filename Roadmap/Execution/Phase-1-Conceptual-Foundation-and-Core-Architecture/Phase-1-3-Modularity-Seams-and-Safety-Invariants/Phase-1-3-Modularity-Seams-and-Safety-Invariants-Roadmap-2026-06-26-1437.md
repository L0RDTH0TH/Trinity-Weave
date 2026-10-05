---
title: Phase 1.3 — Modularity Seams and Safety Invariants (Execution)
roadmap-level: secondary
phase-number: 1
subphase-index: "1.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
status: active
priority: high
progress: 45
handoff_readiness: 72
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
- modularity-seams
- safety-invariants
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.3 — Modularity Seams and Safety Invariants (Execution)

Execution secondary for replaceability ports (generation / rules / bus / input) plus SeedSnapshot → DryRun → Provenance gate chain. Parallel spine under `Roadmap/Execution/Phase-1-…/Phase-1-3-…/`. **No Half B.** L5/SERIES are **read-only advisory feedstock** — seams + safety path **enable** DM-retconnable commit and seat-gated intent parsers (world-shell consumers).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Typed seam ports + pre-commit safety path (snapshot → dry-run → stamp) |
| Inspiration / L5 bar (advisory) | Every world-hitting change DM-retconnable via dry-run fail; IntentParserPort seat-routes; no silent world write |
| Inspiration (studied) | (1) Conceptual 1.3 + tertiaries 1.3.1–1.3.3. (2) Execution 1.1 Bus+Canon. (3) Execution 1.2 StageOrchestrator / DeterministicCompiler. |
| Execution mechanism | GDScript interfaces + pseudo for SeamRegistry, four port families, SeedSnapshotAuthority, DryRunValidator, ProvenanceRecorder |
| Validation signal | Catalog paint DoD met; next paint tertiaries 1.3.1–1.3.3 |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Frozen conceptual 1.3 + tertiaries 1.3.1–1.3.3 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Safety enablement | snapshot→dry-run→provenance before world write; IntentParserPort → CanonCommitBoundary |
| `does_not_mandate` | Autoload SeamRegistry; DryRun world writes; IntentParser bypassing canon/seat |
| Pin color keys | Foundation Cyan · Blue (Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Every world-hitting change DM-retconnable | `safety_commit_path` + DryRunValidator | dry-run fail → ERR_BUSY | dry_run_fail |
| Players do not author first world | `IIntentParserPort.parse` → CanonCommitBoundary | seat refuse + not accepted | IntentEnvelope |
| Table can shape (published seams) | `SeamRegistry.publish` / swap ports | unpublished seam → reject | seam_published |
| Deterministic living world | SeedSnapshotAuthority.capture | missing snapshot → fail | snapshot_sealed |
| Collaborative GUI / Phase-2 | StageExecutorPort swap | preserve 1.2.1 type names | provenance stamp |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SeamRegistry` | Canonical index: seam_id → port owner → swap contract → lifecycle |
| `StageExecutorPort` | Per-stage replaceable executor behind 1.2.1 I/O types |
| `RulePluginPort` | Ruleset plugin hook points + conflict policy declaration |
| `BusSubscriptionPort` | Category-scoped sim/canon subscribers (no bus ownership) |
| `IntentParserPort` | Intent envelope parsers (voice/forms/chat) without Simulation rewrite |
| `SeedSnapshotAuthority` | Immutable pre-mutation capture; session vault retention |
| `DryRunValidator` | Read-only preflight + estimate-only compile; no world write |
| `ProvenanceRecorder` | Stamp ProvenanceEnvelope on commit artifacts |

## Interfaces

```text
enum SeamFamily { GENERATION, RULES, BUS, INPUT }
enum SeamLifecycle { DRAFT, PUBLISHED, DEPRECATED }

SeamEntry (Dictionary schema):
  seam_id: StringName
  family: SeamFamily
  port_owner: StringName
  swap_contract: Dictionary  # {replaceable_unit, neighbor_guarantee}
  lifecycle: SeamLifecycle
  layer_owner: StringName  # WorldState|Simulation|Presentation|InputIntent

SeamRegistry (RefCounted, session-scoped — NOT Autoload):
  + publish(entry: Dictionary) -> Error
  + get(seam_id: StringName) -> Dictionary
  + list_family(family: SeamFamily) -> Array[Dictionary]
  + assert_published(seam_id: StringName) -> Error
  signals: seam_published(seam_id), seam_rejected(seam_id, reason)

IStageExecutorPort (RefCounted):
  + stage_id() -> int  # StageId from 1.2
  + run(upstream: Dictionary, weights: Dictionary) -> Dictionary

IRulePluginPort (RefCounted):
  + ruleset_id() -> StringName
  + hook_points() -> PackedStringArray
  + conflict_policy() -> Dictionary
  + apply_hooks(context: Dictionary) -> Error

IBusSubscriptionPort (RefCounted):
  + allowed_categories() -> PackedStringArray  # e.g. sim.*, canon.*
  + on_event(category: StringName, payload: Dictionary) -> void

IIntentParserPort (RefCounted):
  + parser_id() -> StringName
  + parse(raw: Variant) -> Dictionary  # IntentEnvelope shape; must hit CanonCommitBoundary

SeedSnapshot (RefCounted):
  + fingerprint: String
  + tone_profile_id: StringName
  + accepted_fact_hash: String
  + ruleset_ids: PackedStringArray
  + captured_unix: int
  + to_dict() -> Dictionary

SeedSnapshotAuthority (RefCounted):
  + capture(session: Node, trigger: SnapshotTrigger) -> Dictionary  # {ok:bool, snapshot:SeedSnapshot, error:Error}
  + restore(fingerprint: String) -> Error
  + last_sealed() -> SeedSnapshot
  signals: snapshot_sealed(fingerprint), snapshot_restore_requested(fingerprint), snapshot_failed(reason)

DryRunValidator (RefCounted):
  + validate(request: Dictionary, snapshot: SeedSnapshot) -> Dictionary
  # returns { outcome: "pass"|"fail"|"estimate_only", reasons: PackedStringArray, estimate: Dictionary }
  signals: dry_run_pass(request_id), dry_run_fail(request_id, reasons), dry_run_estimate(request_id)

ProvenanceEnvelope (Dictionary schema):
  stage_executor_id: StringName
  ruleset_id: StringName
  seed_fingerprint: String
  tone_profile_id: StringName
  snapshot_fingerprint: String

ProvenanceRecorder (RefCounted):
  + stamp(artifact: Dictionary, envelope: Dictionary) -> Dictionary
  signals: provenance_stamped(artifact_id)
```

## Pseudo-code

```pseudo
# Phase 1.3 — Seams + safety path (Godot 4 stable Error/OK + signals).
# Citations: docs.godotengine.org/en/stable/ (RefCounted, Node, Dictionary, signals, GlobalScope.Error).
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# Commit order: snapshot seal → dry-run pass → provenance stamp → world write (DM-retconnable).
# DryRunValidator: ZERO world writes — estimate only.
# IIntentParserPort MUST route through CanonCommitBoundary + seat check — players do not author.
# SeamRegistry / DryRun / SeedSnapshotAuthority = session-scoped — NEVER Autoload.
# StageExecutorPort swap preserves 1.2.1 manifest type names (Phase-2 WorldShell).
# ===========================================================

class_name SeamRegistry
extends RefCounted

signal seam_published(seam_id)
signal seam_rejected(seam_id, reason)

var _entries: Dictionary = {}  # StringName -> Dictionary

func publish(entry: Dictionary) -> Error:
	if not entry.has_all(["seam_id", "family", "port_owner", "swap_contract", "lifecycle"]):
		seam_rejected.emit(entry.get("seam_id", &""), "schema")
		return ERR_INVALID_PARAMETER
	var sid: StringName = entry["seam_id"]
	_entries[sid] = entry.duplicate(true)
	if entry["lifecycle"] == SeamLifecycle.PUBLISHED:
		seam_published.emit(sid)
	return OK

func assert_published(seam_id: StringName) -> Error:
	if not _entries.has(seam_id):
		return ERR_DOES_NOT_EXIST
	if _entries[seam_id]["lifecycle"] != SeamLifecycle.PUBLISHED:
		return ERR_UNAVAILABLE
	return OK


class_name SeedSnapshotAuthority
extends RefCounted

signal snapshot_sealed(fingerprint)
signal snapshot_failed(reason)

var _last: SeedSnapshot

func capture(session: Node, trigger: SnapshotTrigger) -> Dictionary:
	# JUNIOR WORK-ORDER: immutable pre-mutation capture before any world-hitting change
	var snap := SeedSnapshot.new()
	var err := _fill_from_session(session, snap, trigger)
	if err != OK:
		snapshot_failed.emit("fill")
		return { "ok": false, "error": err }
	_last = snap
	snapshot_sealed.emit(snap.fingerprint)
	return { "ok": true, "snapshot": snap, "error": OK }


class_name DryRunValidator
extends RefCounted

signal dry_run_pass(request_id)
signal dry_run_fail(request_id, reasons)

var _dag: RefCounted  # DAGValidator from 1.2
var _compiler: RefCounted  # DeterministicCompiler estimate-only
var _registry: SeamRegistry

func validate(request: Dictionary, snapshot: SeedSnapshot) -> Dictionary:
	# JUNIOR WORK-ORDER: ZERO world writes — DM can retcon on fail
	var rid: StringName = request.get("request_id", &"anon")
	var reasons: PackedStringArray = []
	if snapshot == null:
		reasons.append("missing_snapshot")
		dry_run_fail.emit(rid, reasons)
		return { "outcome": "fail", "reasons": reasons, "estimate": {} }
	if _registry.assert_published(request.get("primary_seam", &"")) != OK and request.has("primary_seam"):
		reasons.append("seam_not_published")
	var dag_err: Error = _dag.preflight(request.get("edges", []))
	if dag_err != OK:
		reasons.append("dag_preflight")
	var est: Dictionary = _compiler.compile(
		request.get("bundle"),
		request.get("manifests", {}),
		request.get("hooks", [])
	)
	if not reasons.is_empty():
		dry_run_fail.emit(rid, reasons)
		return { "outcome": "fail", "reasons": reasons, "estimate": est }
	dry_run_pass.emit(rid)
	return { "outcome": "pass", "reasons": reasons, "estimate": est }


func safety_commit_path(session: Node, request: Dictionary, auth: SeedSnapshotAuthority, dry: DryRunValidator, prov: ProvenanceRecorder) -> Error:
	# JUNIOR WORK-ORDER: snapshot → dry-run → stamp → then world write (never reverse)
	var cap: Dictionary = auth.capture(session, request.get("trigger", SnapshotTrigger.WORLD_MANIFEST_COMMIT))
	if not cap["ok"]:
		return cap["error"]
	var result: Dictionary = dry.validate(request, cap["snapshot"])
	if result["outcome"] != "pass":
		return ERR_BUSY  # DM-retconnable abort
	var env := {
		"stage_executor_id": request.get("stage_executor_id", &"default"),
		"ruleset_id": request.get("ruleset_id", &""),
		"seed_fingerprint": cap["snapshot"].fingerprint,
		"tone_profile_id": cap["snapshot"].tone_profile_id,
		"snapshot_fingerprint": cap["snapshot"].fingerprint,
	}
	prov.stamp(request.get("artifact", {}), env)
	return OK
```

## Research integration

Reuse [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]] — session-scoped composition, `Error`/`OK`, signal patterns. Stable docs prefixes only (`docs.godotengine.org/en/stable/`). No new Research Task this wave.

## Children (DFS)

| Index | Note | Status |
|-------|------|--------|
| 1.3.1 | SeamRegistry Canonical Index (execution) | minted (next paint) |
| 1.3.2 | SeedSnapshotAuthority Contract (execution) | minted |
| 1.3.3 | DryRunValidator + ProvenanceEnvelope (execution) | minted |

## Invariants

| ID | Rule |
|----|------|
| I-1.3-001 | SeamRegistry / DryRunValidator / SeedSnapshotAuthority are session-scoped — **never** Autoload |
| I-1.3-002 | DryRunValidator performs **zero** world writes |
| I-1.3-003 | Commit path order: snapshot seal → dry-run pass → provenance stamp → world write |
| I-1.3-004 | IntentParserPort outputs must route through CanonCommitBoundary (1.1.2) |
| I-1.3-005 | StageExecutorPort preserves 1.2.1 manifest type names on swap |

## Acceptance (execution secondary)

- [x] Four port families named with swap contracts
- [x] Safety path pseudo compiles mentally against Error/OK
- [x] conceptual_counterpart resolves to frozen 1.3
- [x] Tertiaries 1.3.1–1.3.3 minted on parallel spine
- [x] **UX Catalog paint** — L5 seats/guards as JUNIOR WORK-ORDER (gold pattern)

## Next

`deepen_complete: true` + **`paint_status: painted`** (`exec-ux-paint-20260929`). Next paint: **1.3.1**.
