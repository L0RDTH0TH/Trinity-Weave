---
title: Phase 1.1.2 — Bus Category Registry and CanonCommitBoundary (Execution)
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.2"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]'
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
- bus-registry
- canon-commit
- execution
- pkg_world_shell
- paint_ux_catalog
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Decoupling-and-Interface-Contracts/Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]'
- '[[ux_world_generation]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_world_generation/L5]]'
- '[[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]'
---

# Phase 1.1.2 — Bus Category Registry and CanonCommitBoundary (Execution)

Execution tertiary: bus taxonomy + read-only canon gate. Parallel spine. **No Half B.** L5/SERIES are **read-only advisory feedstock** — bus topics + propose→accept→hook **enable** world-shell seats/guards (not a new L5 mint).

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Topic namespaces + propose→accept→hook before any Simulation write |
| Inspiration / L5 bar (advisory) | Players do not author first world; every world-hitting change DM-retconnable — enforced at accept/hook + SimWriteGuard |
| Inspiration (studied) | (1) [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]] — canon pipeline `proposed → accepted → hooked → sim-active`. (2) [[1-Projects/genesis-mythos-master/Roadmap/Conceptual-Decision-Records/deepen-layer-decoupling-2026-06-26-1200]] — bus category nouns. (3) [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]] — signal mediation. |
| Execution mechanism | `BusCategoryRegistry` + `CanonCommitBoundary` as injected RefCounted/Object services |
| Validation | Catalog paint DoD met; SimWriteGuard refuses non-hooked facts |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_world_generation` (advisory) |
| `package_id` | `pkg_world_shell` (advisory) |
| `l5_path` (read-only) | `Roadmap/User-Story/scopes/ux_world_generation/L5.md` |
| `conceptual_pin` | Conceptual 1.1.2 |
| `dispatch_scope` | **paint_ux_catalog** deepen (balance); nested little-val during paint |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only advisory) |
|-------|-----------------------------------------------|
| `row_id` | `ux_world_generation` |
| Seats | `shared_table`, `dm_as_player`, `privileged_access` |
| Bus enablement | `session.*` / `canon.*` / `presentation.*` carry scaffold + seat residues to Phase-2 WorldShell / ux_worldgen_gui |
| `does_not_mandate` | players author first world; silent sim write before hook; Autoload canon |
| Pin color keys | Foundation Cyan · Blue (Phase-2) |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| Players do not author first world | `accept` + SeatContext | wrong seat → ERR_UNAUTHORIZED | fact_rejected |
| Durable truth before sim | `hook` then `is_sim_write_allowed` | propose-only → ERR_UNAUTHORIZED | HOOKED |
| Table can shape (dialogue bus) | `session.*` / `presentation.*` topics | owner conflict → category_rejected | categories_ready |
| Every world-hitting change DM-retconnable | reject path + no silent merge | — | fact_rejected / provenance |
| Collaborative GUI signals | presentation.* publish | assert_topic | scaffold preview ready |

## Interfaces

```text
BusCategoryRegistry:
  + bootstrap_default_manifest() -> Error
    # registers canon.* sim.* session.* presentation.*
  + register_category(ns: StringName, owner: LayerId) -> Error
  + assert_topic(topic: StringName, publisher: LayerId) -> Error
  signals: categories_ready(), category_rejected(topic, reason)

CanonCommitBoundary:
  + propose(fact: Dictionary) -> Dictionary   # dry-run; no side effects
  + accept(fact_id: StringName) -> Error
  + hook(fact_id: StringName) -> Error
  + is_accepted(fact_id: StringName) -> bool
    # true iff stage in {ACCEPTED, HOOKED} — generation / intent reads
  + is_sim_write_allowed(fact_id: StringName) -> bool
    # true iff stage == HOOKED only — Simulation mutators
  signals: fact_proposed, fact_rejected, fact_accepted, fact_hooked

SimWriteGuard (thin helper on SimulationLayer):
  + apply_if_allowed(boundary, fact_id, mutator: Callable) -> Error
```

## Pseudo-code

```pseudo
# 1.1.2 — Bus + CanonCommitBoundary (Godot 4 stable).
#
# === JUNIOR WORK-ORDER (ux_world_generation L5 — advisory) ===
# Own the gate: propose (dry-run) → accept (author seat) → hook → sim write.
# Players do not author first world — accept refuses player seat.
# session.* / presentation.* bus carries ux_worldgen_gui scaffold residues to Phase-2.
# Anti-mandate: never silent Simulation mutate on PROPOSED/ACCEPTED-only facts.
# ===========================================================

func bootstrap_default_manifest() -> Error:
	# JUNIOR WORK-ORDER: register topics Phase-2 WorldShell / GUI will publish on
	var pairs := [
		[&"canon.*", LayerId.INPUT_INTENT],
		[&"sim.*", LayerId.SIMULATION],
		[&"session.*", LayerId.WORLD_STATE],
		[&"presentation.*", LayerId.PRESENTATION],
	]
	for p in pairs:
		var err := register_category(p[0], p[1])
		if err != OK:
			return err
	categories_ready.emit()
	return OK

func accept(fact_id: StringName) -> Error:
	# JUNIOR WORK-ORDER: refuse player seat — table/DM only for lasting world truth
	if _seat != null and not _seat.allows_any(["shared_table", "dm_as_player", "privileged_access"]):
		fact_rejected.emit(fact_id, "wrong_seat")
		return ERR_UNAUTHORIZED
	if _stage.get(fact_id) != Stage.PROPOSED:
		fact_rejected.emit(fact_id, "not_proposed")
		return ERR_INVALID_PARAMETER
	_stage[fact_id] = Stage.ACCEPTED
	fact_accepted.emit(fact_id)
	return OK

func is_accepted(fact_id: StringName) -> bool:
	# Dual-gate: generation/intent may read ACCEPTED|HOOKED (Phase-2 pipeline)
	var st = _stage.get(fact_id, Stage.PROPOSED)
	return st == Stage.ACCEPTED or st == Stage.HOOKED

func is_sim_write_allowed(fact_id: StringName) -> bool:
	# JUNIOR WORK-ORDER: world-hitting sim requires HOOKED — DM-retconnable promote path
	return _stage.get(fact_id, Stage.PROPOSED) == Stage.HOOKED

func apply_if_allowed(boundary: CanonCommitBoundary, fact_id: StringName, mutator: Callable) -> Error:
	if not boundary.is_sim_write_allowed(fact_id):
		return ERR_UNAUTHORIZED
	mutator.call()
	return OK

# propose() MUST NOT touch WorldState or Simulation — estimate Dictionary only.
```

## Edge-case ACs

- [ ] `propose` then immediate Simulation mutate → `ERR_UNAUTHORIZED` (not hooked)
- [ ] Rejected proposal never reaches `ACCEPTED` / `HOOKED`
- [ ] Owner conflict on `register_category` → `category_rejected` + `ERR_ALREADY_IN_USE`
- [ ] Dry-run rejection emits `fact_rejected` with zero WorldState appends
- [x] **UX Catalog paint** — L5 seats/guards as JUNIOR WORK-ORDER (gold pattern)

## Research integration

> "A Callable is a built-in Variant type that represents a method or a standalone function."
> — https://docs.godotengine.org/en/stable/classes/class_callable.html

> "Nodes which are siblings should only be aware of their own hierarchies while an ancestor mediates their communications and references."
> — https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

> "To use signals you need to connect them first…"
> — https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html

> "OK = 0 — Methods that return Error return OK when no error occurred."
> — https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#enum-globalscope-error

Links: [[Ingest/Agent-Research/godot-phase1-layer-decoupling-citations-gmm-2026-09-29-0144]]

## Status

`deepen_complete: true` + **`paint_status: painted`** (`exec-ux-paint-20260929`). Next paint: **1.1.3**.
