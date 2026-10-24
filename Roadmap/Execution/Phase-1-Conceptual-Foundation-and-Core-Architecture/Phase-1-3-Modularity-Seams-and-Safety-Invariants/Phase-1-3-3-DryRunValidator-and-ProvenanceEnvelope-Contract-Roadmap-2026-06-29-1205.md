---
title: Phase 1.3.3 — DryRunValidator and ProvenanceEnvelope Contract (Execution)
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.3.3"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-3-DryRunValidator-and-ProvenanceEnvelope-Contract-Roadmap-2026-06-29-1205]]'
status: active
priority: high
progress: 55
handoff_readiness: 76
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
- dry-run-validator
- provenance
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-3-DryRunValidator-and-ProvenanceEnvelope-Contract-Roadmap-2026-06-29-1205]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline/Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.3.3 — DryRunValidator and ProvenanceEnvelope Contract (Execution)

Execution tertiary: gate matrix, check catalog, estimate-only compile, ProvenanceEnvelope stamp on commit. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — dry-run fail **enables** DM-retconnable block before persist. Closes Phase **1.3** / Phase **1** paint tree.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Read-only pre-commit gate + provenance stamp after pass |
| Inspiration / L5 bar (advisory) | World-hitting commits blocked on dry-run fail; zero writes in validate; provenance after pass only |
| Inspiration (studied) | (1) Conceptual 1.3.3 + rollup. (2) Execution 1.2 DeterministicCompiler / DAGValidator. (3) Execution 1.3.2 sealed snapshot prerequisite. |
| Execution mechanism | `DryRunValidator` check catalog + `ProvenanceRecorder`; bus events `session.dry_run_*` |
| Validation | Catalog paint DoD met; Phase 1 paint tree complete → Phase 3 |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Conceptual 1.3.3 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Safety enablement | snapshot→dry-run→provenance→persist; fail = DM-retconnable block |
| `does_not_mandate` | world write inside validate; Autoload DryRunValidator; stamp before pass |
| Pin color keys | Foundation Cyan · Blue (Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Every world-hitting change DM-retconnable | `safety_commit` + dry-run fail | ERR_BUSY on fail | dry_run_fail |
| Deterministic living world | EstimateOnlyCompiler | zero persist in validate | estimate Dictionary |
| Players do not author first world | CheckCatalog + accepted snapshot | missing_snapshot → fail | session.dry_run_* |
| Table can shape (published seams) | seam_not_published check | CompletenessGate | dry_run_fail |
| Collaborative audit | ProvenanceRecorder.stamp | only after pass | provenance_stamped |

## Module map

| Module | Responsibility |
|--------|----------------|
| `DryRunValidator` | Ordered check catalog; emit pass/fail/estimate_only |
| `CheckCatalog` | DAG, rule conflicts, spatial estimate, unreachable NPC refs |
| `EstimateOnlyCompiler` | DeterministicCompiler branch — no persist |
| `ProvenanceEnvelope` | Field schema on artifacts |
| `ProvenanceRecorder` | Stamp on successful commit only |

## Interfaces

```text
enum DryRunOutcome { PASS, FAIL, ESTIMATE_ONLY }

DryRunRequest (Dictionary):
  request_id: StringName
  trigger: SnapshotTrigger
  edges: Array
  bundle: RefCounted
  manifests: Dictionary
  hooks: Array
  primary_seam: StringName
  stage_executor_id: StringName
  ruleset_id: StringName
  artifact: Dictionary

CheckCatalog (RefCounted):
  + run_all(request: Dictionary, snapshot: SeedSnapshot) -> PackedStringArray

DryRunValidator (RefCounted):
  + validate(request: Dictionary, snapshot: SeedSnapshot) -> Dictionary
  signals: dry_run_pass(request_id), dry_run_fail(request_id, reasons), dry_run_estimate(request_id)

ProvenanceRecorder (RefCounted):
  + stamp(artifact: Dictionary, envelope: Dictionary) -> Dictionary
  + read(artifact_id: StringName) -> Dictionary
  signals: provenance_stamped(artifact_id)
```

### Gate matrix (operations requiring dry-run)

| Operation | Snapshot (1.3.2) | Dry-run | On fail |
|-----------|------------------|---------|---------|
| CompiledWorldManifest commit | sealed | required | block + DM cite |
| DM structural regen | sealed | required | block |
| Ruleset swap (live) | sealed | required | block |
| Seam swap mid-session | sealed | required | abort DAG |

### Check catalog (ordered)

| Ordinal | Check | Fail reason code |
|---------|-------|------------------|
| 1 | Snapshot non-null + fingerprint match session | `missing_snapshot` |
| 2 | SeamRegistry CompletenessGate / primary_seam PUBLISHED | `seam_not_published` |
| 3 | DAGValidator.preflight | `dag_preflight` |
| 4 | Rule conflict scan (RulePluginPort declarations) | `rule_conflict` |
| 5 | Spatial overlap estimate (read-only) | `spatial_overlap` |
| 6 | Unreachable NPC / entity refs | `unreachable_ref` |
| 7 | Estimate-only compile | `estimate_compile` (soft → ESTIMATE_ONLY if partial ok) |

**Bus events (session.*):** `session.dry_run_pass`, `session.dry_run_fail`, `session.dry_run_estimate` — align with 1.1 category registry; never Autoload-global gameplay.

### ProvenanceEnvelope fields

| Field | Type | Source |
|-------|------|--------|
| `stage_executor_id` | StringName | request / bound port |
| `ruleset_id` | StringName | active ruleset |
| `seed_fingerprint` | String | SeedSnapshot |
| `tone_profile_id` | StringName | SeedSnapshot |
| `snapshot_fingerprint` | String | SeedSnapshot |
| `dry_run_request_id` | StringName | DryRunRequest |

## Pseudo-code

```pseudo
# 1.3.3 — DryRunValidator + Provenance (Godot 4 stable).
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# validate() = ZERO world / FileAccess writes — estimate only.
# Order: snapshot seal → dry-run pass → provenance stamp → THEN persist.
# dry-run fail → ERR_BUSY = DM-retconnable block (cite reasons to table).
# ProvenanceRecorder.stamp ONLY after pass — never stamp-then-hope.
# Bus: session.dry_run_* from 1.1 registry — never Autoload gameplay.
# ===========================================================

class_name CheckCatalog
extends RefCounted

var _dag: RefCounted
var _registry: SeamRegistry

func run_all(request: Dictionary, snapshot: SeedSnapshot) -> PackedStringArray:
	var reasons: PackedStringArray = []
	if snapshot == null:
		reasons.append("missing_snapshot")
		return reasons
	if request.has("primary_seam"):
		if _registry.assert_published(request["primary_seam"]) != OK:
			reasons.append("seam_not_published")
	if _dag.preflight(request.get("edges", [])) != OK:
		reasons.append("dag_preflight")
	return reasons


class_name DryRunValidator
extends RefCounted

signal dry_run_pass(request_id)
signal dry_run_fail(request_id, reasons)
signal dry_run_estimate(request_id)

var _checks: CheckCatalog
var _compiler: RefCounted

func validate(request: Dictionary, snapshot: SeedSnapshot) -> Dictionary:
	# JUNIOR WORK-ORDER: never persist inside validate
	var rid: StringName = request.get("request_id", &"anon")
	var reasons := _checks.run_all(request, snapshot)
	var estimate: Dictionary = {}
	if _compiler != null and reasons.is_empty():
		estimate = _compiler.compile(
			request.get("bundle"),
			request.get("manifests", {}),
			request.get("hooks", [])
		)
		if estimate.get("incomplete", false) and estimate.get("ok", false):
			dry_run_estimate.emit(rid)
			return { "outcome": "estimate_only", "reasons": reasons, "estimate": estimate }
	if not reasons.is_empty() or not estimate.get("ok", true):
		if not estimate.get("ok", true) and reasons.is_empty():
			reasons.append("estimate_compile")
		dry_run_fail.emit(rid, reasons)  # JUNIOR: DM-retconnable block signal
		return { "outcome": "fail", "reasons": reasons, "estimate": estimate }
	dry_run_pass.emit(rid)
	return { "outcome": "pass", "reasons": reasons, "estimate": estimate }


class_name ProvenanceRecorder
extends RefCounted

signal provenance_stamped(artifact_id)

var _by_id: Dictionary = {}

func stamp(artifact: Dictionary, envelope: Dictionary) -> Dictionary:
	var aid: StringName = artifact.get("id", &"")
	var merged := artifact.duplicate(true)
	merged["provenance"] = envelope.duplicate(true)
	_by_id[aid] = merged["provenance"]
	provenance_stamped.emit(aid)
	return merged


func safety_commit(session: Node, request: Dictionary, auth: SeedSnapshotAuthority, dry: DryRunValidator, prov: ProvenanceRecorder) -> Error:
	# JUNIOR WORK-ORDER: snapshot → dry-run → stamp → persist (never reverse)
	var snap: SeedSnapshot = auth.last_sealed()
	if snap == null:
		var cap := auth.capture(session, request.get("trigger", SnapshotTrigger.WORLD_MANIFEST_COMMIT))
		if not cap["ok"]:
			return cap["error"]
		snap = cap["snapshot"]
	var result := dry.validate(request, snap)
	if result["outcome"] == "fail":
		return ERR_BUSY  # DM-retconnable
	var env := {
		"stage_executor_id": request.get("stage_executor_id", &"default"),
		"ruleset_id": request.get("ruleset_id", &""),
		"seed_fingerprint": snap.fingerprint,
		"tone_profile_id": snap.tone_profile_id,
		"snapshot_fingerprint": snap.fingerprint,
		"dry_run_request_id": request.get("request_id", &"anon"),
	}
	prov.stamp(request.get("artifact", {}), env)
	# ONLY NOW may caller persist CompiledWorldManifest
	return OK
```

## Invariants

| ID | Rule |
|----|------|
| I-1.3.3-001 | `validate()` performs zero world / FileAccess writes |
| I-1.3.3-002 | Provenance stamp only after dry-run pass (or estimate_only with operator ack — Phase 6) |
| I-1.3.3-003 | Ordering: snapshot seal → dry-run → provenance → persist |
| I-1.3.3-004 | Bus emissions use `session.*` categories from 1.1 registry |

## Acceptance

- [x] Gate matrix + check catalog present
- [x] ProvenanceEnvelope fields listed
- [x] conceptual_counterpart → frozen 1.3.3
- [x] Phase 1.3 wave complete on execution spine
- [x] **UX Catalog paint** — L5 seats/guards as JUNIOR WORK-ORDER (gold pattern)

## Status

`deepen_complete: true` + **`paint_status: painted`** (`exec-ux-paint-20260929`). **Phase-1 paint tree COMPLETE.** Next campaign cursor: **Phase-3 primary**.
