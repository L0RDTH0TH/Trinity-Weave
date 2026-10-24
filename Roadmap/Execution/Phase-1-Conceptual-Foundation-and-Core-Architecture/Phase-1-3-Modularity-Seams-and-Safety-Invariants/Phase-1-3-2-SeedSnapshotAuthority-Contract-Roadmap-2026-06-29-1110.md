---
title: Phase 1.3.2 — SeedSnapshotAuthority Contract (Execution)
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.3.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]]'
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
- seed-snapshot
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-2-SeedSnapshotAuthority-Contract-Roadmap-2026-06-29-1110]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.3.2 — SeedSnapshotAuthority Contract (Execution)

Execution tertiary: trigger matrix, SeedSnapshot schema, seal/restore, session vault retention. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — sealed snapshots **enable** DM-retconnable restore before world-hitting commits.

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Immutable pre-mutation snapshot before manifest commit / DM regen / ruleset swap |
| Inspiration / L5 bar (advisory) | Every world-hitting change preceded by seal; accepted facts only; restore = DM-visible retcon |
| Inspiration (studied) | (1) Conceptual 1.3.2 + rollup. (2) Execution 1.3 safety path. (3) 1.1.2 CanonCommitBoundary — accepted facts only. |
| Execution mechanism | `SeedSnapshotAuthority` + `SnapshotVault` (session user:// or session dir) + trigger matrix |
| Validation | Catalog paint DoD met; CompletenessGate before capture |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Conceptual 1.3.2 + rollup |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Snapshot enablement | Seal before commit/regen/swap; restore invalidates event log (DM-visible) |
| `does_not_mandate` | proposed facts in fingerprint; Autoload vault; capture without CompletenessGate |
| Pin color keys | Foundation Cyan · Blue (Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Every world-hitting change DM-retconnable | `capture` before commit/regen | registry_incomplete → fail | snapshot_sealed |
| Players do not author first world | `accepted_fact_hash` only | proposed excluded | fingerprint |
| Deterministic living world | SeedSnapshot fields | session vault only | SnapshotVault |
| Table/DM restore | `restore` + event_log_tail_invalidated | missing → ERR_DOES_NOT_EXIST | DM-visible |
| Collaborative GUI | session-scoped paths | not Autoload | user://session_* |

## Module map

| Module | Responsibility |
|--------|----------------|
| `SeedSnapshot` | Immutable field bag + fingerprint |
| `SeedSnapshotAuthority` | capture / seal / restore / last_sealed |
| `SnapshotVault` | Persist last N snapshots under session scope |
| `TriggerMatrix` | Which operations require capture |

## Interfaces

```text
enum SnapshotTrigger {
  WORLD_MANIFEST_COMMIT,
  DM_STRUCTURAL_REGEN,
  RULESET_SWAP_LIVE,
  SEAM_SWAP_MID_SESSION
}

SeedSnapshot (RefCounted):
  + fingerprint: String
  + tone_profile_id: StringName
  + accepted_fact_hash: String
  + ruleset_ids: PackedStringArray
  + seam_registry_hash: String
  + trigger: SnapshotTrigger
  + captured_unix: int
  + to_dict() -> Dictionary
  + from_dict(d: Dictionary) -> Error

SnapshotVault (RefCounted):
  + store(snapshot: SeedSnapshot) -> Error
  + load_latest() -> SeedSnapshot
  + load(fingerprint: String) -> SeedSnapshot
  + retain_last(n: int) -> void

SeedSnapshotAuthority (RefCounted):
  + capture(session: Node, trigger: SnapshotTrigger) -> Dictionary
  + restore(fingerprint: String) -> Error
  + last_sealed() -> SeedSnapshot
  + require_before(trigger: SnapshotTrigger) -> bool
  signals: snapshot_sealed(fingerprint), snapshot_restore_requested(fingerprint),
           snapshot_failed(reason), event_log_tail_invalidated(from_unix)
```

### Trigger matrix

| Trigger | Capture required | Notes |
|---------|------------------|-------|
| WORLD_MANIFEST_COMMIT | yes | Before DeterministicCompiler persist |
| DM_STRUCTURAL_REGEN | yes | Before StageOrchestrator re-run |
| RULESET_SWAP_LIVE | yes | After SeamRegistry assert on rules.plugin.* |
| SEAM_SWAP_MID_SESSION | yes | Abort in-flight DAG; restart from last seal |

**Ordering vs 1.3.1:** `CompletenessGate.check == OK` before any `gen.stage.*` capture. **Canon:** snapshot includes **accepted** CanonFacts hash only (proposed excluded — 1.1.2).

## Pseudo-code

```pseudo
# 1.3.2 — SeedSnapshotAuthority (Godot 4 stable).
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# Capture BEFORE any world-hitting commit/regen/swap — DM-retconnable restore path.
# Fingerprint uses accepted_fact_hash ONLY — proposed never enters (players do not author).
# CompletenessGate first — unpublished seams → snapshot_failed("registry_incomplete").
# Restore emits event_log_tail_invalidated — DM-visible retcon, not silent rewrite.
# Vault is session-scoped — NEVER Autoload gameplay singleton.
# ===========================================================

class_name SnapshotVault
extends RefCounted

var _dir: String  # set by SessionComposer
var _retention: int = 5
var _index: Array = []  # fingerprints newest-first

func store(snapshot: SeedSnapshot) -> Error:
	if _dir.is_empty():
		return ERR_UNCONFIGURED
	_index.push_front(snapshot.fingerprint)
	retain_last(_retention)
	return OK

func load_latest() -> SeedSnapshot:
	if _index.is_empty():
		return null
	return load(_index[0])


class_name SeedSnapshotAuthority
extends RefCounted

signal snapshot_sealed(fingerprint)
signal snapshot_failed(reason)
signal event_log_tail_invalidated(from_unix)

var _vault: SnapshotVault
var _registry: SeamRegistry
var _last: SeedSnapshot

func capture(session: Node, trigger: SnapshotTrigger) -> Dictionary:
	# JUNIOR WORK-ORDER: gate seams before seal — no world commit on incomplete registry
	if CompletenessGate.new().check(_registry) != OK:
		snapshot_failed.emit("registry_incomplete")
		return { "ok": false, "error": ERR_UNAVAILABLE }
	var snap := SeedSnapshot.new()
	snap.trigger = trigger
	snap.captured_unix = int(Time.get_unix_time_from_system())
	snap.tone_profile_id = session.get_meta("tone_profile_id", &"medium_fantasy")
	# JUNIOR WORK-ORDER: accepted facts only — proposed excluded
	snap.accepted_fact_hash = _hash_accepted_facts(session)
	snap.ruleset_ids = _active_rulesets(session)
	snap.seam_registry_hash = _hash_registry(_registry)
	snap.fingerprint = _fingerprint(snap)
	var err := _vault.store(snap)
	if err != OK:
		snapshot_failed.emit("vault")
		return { "ok": false, "error": err }
	_last = snap
	snapshot_sealed.emit(snap.fingerprint)
	return { "ok": true, "snapshot": snap, "error": OK }

func restore(fingerprint: String) -> Error:
	var snap: SeedSnapshot = _vault.load(fingerprint)
	if snap == null:
		snapshot_failed.emit("missing")
		return ERR_DOES_NOT_EXIST
	# JUNIOR WORK-ORDER: DM-visible retcon — invalidate event log tail
	event_log_tail_invalidated.emit(snap.captured_unix)
	_last = snap
	return OK
```

## Invariants

| ID | Rule |
|----|------|
| I-1.3.2-001 | At least one sealed snapshot before first world commit |
| I-1.3.2-002 | Proposed CanonFacts never enter fingerprint inputs |
| I-1.3.2-003 | Restore invalidates event log tail (DM-visible) |
| I-1.3.2-004 | Vault is session-scoped — not project Autoload singleton state |

## Acceptance

- [x] Trigger matrix covered
- [x] Registry completeness gate before capture
- [x] conceptual_counterpart → frozen 1.3.2
- [x] **UX Catalog paint** — L5 seats/guards as JUNIOR WORK-ORDER (gold pattern)

## Status

`deepen_complete: true` + **`paint_status: painted`** (`exec-ux-paint-20260929`). Next paint: **1.3.3**.
