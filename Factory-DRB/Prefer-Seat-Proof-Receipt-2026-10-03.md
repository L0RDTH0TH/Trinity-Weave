---
title: Prefer Seat Proof Receipt — s1 occupancy (topology seat, hostile pass)
created: 2026-10-03
updated: 2026-10-03
project-id: genesis-mythos-master
status: active
slice_id: alpha0_townscaper_tutorial_s1_occupancy_r1
claim_class: staging
go_latch_reverted_at: 2026-10-03T03:45:00Z
tags: [factory, prefer, proof-receipt, topology, hostile-validation]
---

# Prefer Seat Proof Receipt — `alpha0_townscaper_tutorial_s1_occupancy_r1`

**Run:** 2026-10-03T03:12Z · read-only · no Code-Repos write · no Curator push.
**Amended 2026-10-03T03:45Z:** the GO-latch section of this receipt is **retracted**. The `operator_go` / `do_not_auto_dispatch` staging gate it documented was built from misreading the operator's "say GO" as a harness word-gate; it only blocked factory staging and has been removed. The topology proofs below stand unchanged — that seat was the real fix.
**Purpose:** make the *mechanical* Prefer seat legible on a surface Grok can read. `scripts/**` is **not** published to `project/*` branches, so law text alone was unfalsifiable from Grok's side. This receipt carries the executed evidence.

Law under test: [[Prefer-Authorship-Host-Law]] § C · § D · [[Grid-Topology-Host-Law]].
Harness (vault-only): `scripts/eat_queue_core/weave/factory/prefer_authorship_contract.py` · `implicit_intent_bind.py` · `factory_pq_stage.py`.

## Proof A — Prefer executed against current LIVE; hard-fails

`run_prefer_authorship_pass(vault_root, lane_id="module", game_repo_rel="5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos", job={slice_id, project_id, armed_packet_path, prefer_proof, do_not_waive=PRODUCT_PREFER_DO_NOT_WAIVE})`

```
ok          = False
applicable  = True
warnings    = ()              # dict step-1 lock resolved; no bool-underspecified warning
bind        = implicit_bind_ok · topology_rewrite = True
              .technical/weave/factory/genesis-mythos-master/alpha0_townscaper_tutorial_s1_occupancy_r1/implicit-intent-bind.json
```

All three non-waivable topology refuses fired:

```
explicit_met_implicit_miss:topology_axes_missing:edges+faces_cells
points_as_grid:logic_points:Core/WorldGen/ICraftCellAuthority.cs,
               logic_points:Systems/DualGridCraftHost.cs,
               marker_per_point:Systems/DualGridCraftHost.cs,
               point_array:Core/WorldGen/Hex19OccupancyLattice.cs
count_equals_topology:point_count:Core/WorldGen/Hex19OccupancyLattice.cs,
                      point_count:Systems/DualGridCraftHost.cs
```

`topology_evidence` (structured, from the seat receipt — not a bool):

```json
{
  "repo_present": true,
  "files_scanned": ["Core/WorldGen/Hex19OccupancyLattice.cs",
                    "Core/WorldGen/ICraftCellAuthority.cs",
                    "Systems/DualGridCraftHost.cs",
                    "Systems/WorldgenCraft.cs"],
  "required_live_files_present": ["Systems/DualGridCraftHost.cs",
                                  "Core/WorldGen/Hex19OccupancyLattice.cs"],
  "required_live_files_absent": [],
  "edge_signals": [],
  "face_cell_signals": [],
  "point_signals": ["logic_points:Core/WorldGen/ICraftCellAuthority.cs",
                    "logic_points:Systems/DualGridCraftHost.cs",
                    "marker_per_point:Systems/DualGridCraftHost.cs",
                    "point_array:Core/WorldGen/Hex19OccupancyLattice.cs",
                    "point_array:Systems/DualGridCraftHost.cs",
                    "point_count:Core/WorldGen/Hex19OccupancyLattice.cs",
                    "point_count:Systems/DualGridCraftHost.cs"],
  "has_edges": false,
  "has_faces_or_cells": false,
  "points_only": true,
  "missing_axes": ["edges", "faces_cells"]
}
```

**True positive, confirmed by hand.** LIVE `Core/WorldGen/Hex19OccupancyLattice.cs` exposes `PointCount = 19`, `Vector2I[] Points`, `HashSet<Vector2I> PointSet`, `Contains`, `HexDistance`, `AxialToWorld`, `TrySnapWorldToAxial`. There is **no** edge collection, neighbor-adjacency API, cell/corner type, or face builder anywhere in the file. `DualGridCraftHost` renders one `MakeDiskMarker` per point. The prior F5 was a point cloud; `f5_invalidated: points_as_grid__hex19_point_cloud_not_lattice_graph` is accurate.

Note the comment-stripping guard is load-bearing on *real* code, not only on fixtures: the LIVE file contains the comment `// Start at (+ring, 0) and walk the six edges counterclockwise.`, which would otherwise have matched `edge_collection` and falsely cleared the edges axis. `_code_only()` strips it, so `edge_signals` is correctly empty.

## Proof B — RETRACTED (GO latch removed 2026-10-03)

The original Proof B documented a staging latch that refused `IMPLEMENT_SLICE` while `do_not_auto_dispatch: true` and `operator_go` was not `true`, across three "go flip surfaces". That gate was a misreading: "say GO" was an operator **chat** kickoff for a re-eat, never a request for a YAML word-gate. The latch's only real effect was to block the factory from staging s1, so it has been removed along with the `operator_go` / `do_not_auto_dispatch` / `primed_awaiting_go` / `go_flip_surfaces` ritual on every surface.

What replaced it in `factory_pq_stage.py`:

```python
def armed_slice_authority_note(armed, *, slice_id: str = "") -> str:
    """Advisory only — GO is an operator chat kickoff, never a YAML word-gate."""
    armed = armed if isinstance(armed, dict) else {}
    armed_slice = str(armed.get("slice_id") or "")
    if slice_id and armed_slice and armed_slice != slice_id:
        return f"armed_slice_divergence:{armed_slice}!={slice_id}"
    return ""
```

`resolve_authority_armed_packet()` (ex-`resolve_latch_armed_packet`) is kept: sibling `{slice_id}.armed.yaml` first, else the `factory-project.yaml → armed_packet` pointer. It still earns its keep for armed-law context when a stale implementation cell ticks under another `slice_id` — `product_factory.active_slice.id` is still `row_ux_world_generation_r1_d6`, so a composed slice can diverge from s1. That divergence is now reported on the staged result (`armed_slice_divergence`) and does **not** refuse staging.

Staging s1 is unblocked.

## Proof — five Phase-1 exit-gate tests

`python3 -m unittest -v eat_queue_core.tests.test_prefer_authorship_host_law.PreferTopologySeatTests`

```
test_1_points_only_live_scan_fails_prefer ................ ok
test_2_edges_and_cells_pass_topology_axis ................ ok
test_3_missing_bind_fails_prefer .......................... ok
test_4_staging_injects_armed_packet_path .................. ok
test_5_bool_step1_lock_does_not_false_fail ................ ok
Ran 5 tests — OK
```

Full suites `test_prefer_authorship_host_law` + `test_implicit_intent_bind`: **Ran 33 tests — OK** (37 after Proof D added its four).

Seat wiring verified non-dead: `review_pass_runner.PASS_RUNNERS["prefer_authorship_pass"]` → `run_prefer_authorship_pass` (forwards `game_repo_rel`); `lane_agent_registry` force-appends the seat whenever `slice_requires_prefer_authorship` is true, so a lane charter's `review_passes` cannot drop it; the seat is **not** in `TAGGED_STUB_SEATS`, so it cannot auto-pass as untagged.

## Proof D — clean ask cannot disarm the topology axis (added 2026-10-03)

The ask below contains no points / grid / hex wording, so the prose regex does **not** fire. Composed against the real s1 armed packet, the axis still arms from law:

```
explicit_ask            = "Stand up the tutorial step one authoring surface so the operator can
                           place and remove a tile under the mouse and toggle the scaffold overlay."
ask_triggers_topology_rewrite(explicit_ask) = False
ask_triggers_topology_rewrite(slice_id)     = False

topology_rewrite        = True
topology_rewrite_sources = [
  "armed_lock_refuse:step1_authorship:count_equals_topology",
  "armed_lock_refuse:step1_authorship:explicit_met_implicit_miss",
  "armed_lock_refuse:step1_authorship:points_as_grid",
  "armed_prefer_authorship_with_topology_law",
  "armed_structural_topology:done_when",
  "armed_structural_topology:hard_prefer_gaps",
  "armed_structural_topology:step1_authorship.structural_success",
  "armed_structural_topology:step1_occupancy.law"
]
refuse ⊇ points_as_grid · count_equals_topology · infinite_rect_as_hex19 · prop_scatter_as_composition
```

Prefer then runs against the same point-cloud LIVE as Proof A and hard-fails on all three non-waivable codes, with `points_only: true` and `missing_axes: ["edges", "faces_cells"]`.

Hand-disarming the composed bind (`topology_rewrite: false`) does **not** buy a green seat — it buys two extra violations and the LIVE scan still runs:

```
implicit_bind_topology_rewrite_disarmed_vs_armed_law:armed_lock_refuse:…
topology_rewrite_disarmed_on_prefer_slice:alpha0_townscaper_tutorial_s1_occupancy_r1
points_as_grid:… · count_equals_topology:… · explicit_met_implicit_miss:…
```

Tests: `ArmedLawTopologyDerivationTests` + `CleanAskPreferStillFailsLiveTests` in `test_implicit_intent_bind.py` — they read the real armed packet at `1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_townscaper_tutorial_s1_occupancy_r1.armed.yaml` and scan the real LIVE tree at `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/`. Full suites `test_prefer_authorship_host_law` + `test_implicit_intent_bind`: **Ran 37 tests — OK**.

## Residual risks — open, not closed by this receipt

1. ~~**`topology_rewrite` was regex-on-prose.**~~ **Closed 2026-10-03** (see Proof D). The flag is now derived from the resolved armed packet; prose regex is a secondary trigger only, and a bind that disarms the axis fails Prefer closed instead of skipping the LIVE scan.
2. ~~**`armed_gate_blocks_staging` fail-opens three ways.**~~ Moot — the gate was removed (see Proof B). The fail-open analysis was correct, but the right answer was deleting the latch, not hardening it.
3. **Step-1 lock is dual-shaped but currently resolves correctly.** The armed packet carries *both* top-level `step1_authorship: true` and `locks.step1_authorship:` (dict). `resolve_step1_lock` checks `locks.*` first, returns the dict, and emits no warning — confirmed by Proof A (`warnings = ()`). The bare bool is redundant, not harmful. Low risk; cosmetic cleanup only.
4. **No producer receipt for s1 — now the first thing staging hits.** `load_producer_receipt(vault_root, "alpha0_townscaper_tutorial_s1_occupancy_r1")` → `None`, and `implementation_cell.producer_run_id` is still `sp-craft-vis-032901`, which belongs to `alpha0_townscaper_craft_visual` (listed under `supersedes_altitude`). With the armed gate gone, `producer_receipt_missing` is the live refuse for a vault-feed stage, so kickoff **must** force a fresh module-lane compose for s1; a stale compose is the real risk here.
5. **Harness is not visible on `project/*`; `main` refreshed 2026-10-03.** `project/genesis-mythos-master` contains zero `scripts/**` by design (`grok_bridge.project_surfaces` = Factory-DRB + Roadmap + LIVE game repo). Trinity `main` now carries both `scripts/eat_queue_core/weave/factory/prefer_authorship_contract.py` (615 lines) and `implicit_intent_bind.py` (565 lines), byte-identical to vault, via `weave_public_sync` (`scripts/eat_queue_core/weave/` is on the public allowlist). Grok's "can't see the harness" objection was substantively correct and is now addressed for the seat modules. **Still open:** `test_implicit_intent_bind.py` / `test_prefer_authorship_host_law.py` are *not* on the publish allowlist (only `test_weave*` / `test_trinity*` / `test_schedule*` / `test_grok*` / `test_pseudo_clock`), so the proofs remain receipt-only from Grok's side. A committed `__pycache__/*.pyc` on `main` is separate hygiene debt.

## Post-weld requirement (Grok proof C — not performed here)

After the next weld, Prefer **must** be re-run against the new LIVE and the receipt re-attached here. The post-weld pass must show `has_edges: true`, `has_faces_or_cells: true`, `missing_axes: []`, and `ok: true` — with `edge_signals` / `face_cell_signals` naming real code sites. A weld that only grows `point_signals` is `points_as_grid` again regardless of F5 appearance. `claim_class` stays `staging` until operator F5.
