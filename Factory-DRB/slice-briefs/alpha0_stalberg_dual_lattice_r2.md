---
slice_id: alpha0_stalberg_dual_lattice_r2
ask_id: alpha0_stalberg_dual_lattice
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2e
created: 2026-10-03
updated: 2026-10-03
claim_class: staging
factory_greenlit: true
status: staging_prefer_ok_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_dual_lattice_r1
supersedes: alpha0_stalberg_dual_lattice_r1
logic_prior_slice_id: alpha0_stalberg_dual_corner_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_craft_plane_authority_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_lattice_r2.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
success_object: dual_offset_cells
intent_invariant: "Player edits logic points; dual cells are the half-offset quads whose corners are those points."
---

# Slice brief — `alpha0_stalberg_dual_lattice_r2`

**GREENLIT** `2026-10-03T23:54:41Z` — product rewrite of dual-lattice altitude with full conceptual leg + Prefer **concept** path (object identity + invariant). Supersedes [[alpha0_stalberg_dual_lattice_r1]] (staging Prefer / symbols-only; no concept Prefer). claim_class staging until operator F5.

## Project end-state (craft-plane north star)

Player paints **logic points** on the organic craft plane; the living world ownership graph is the **half-step dual lattice** — dual cells (Varignon / half-offset quads) whose corners are those logic points. Cyan debug / occupancy updates sit on `d_*` dual tiles around a clicked point, never a primary-face 2×2. Dual-visual art and density ride this graph later; craft-plane authority and organic underlay stay.

## Path position

| Leg | Slice | Role |
|-----|-------|------|
| Last green wrong-object | [[alpha0_stalberg_dual_neighborhood_r1]] | Stable ≤4 of **primary faces** (cyan 2×2) |
| Prior lattice attempt | [[alpha0_stalberg_dual_lattice_r1]] | Half-step weld + Prefer symbols; **superseded** — staging Prefer without concept Prefer / conceptual leg |
| **This** | `alpha0_stalberg_dual_lattice_r2` | Half-step dual lattice **ownership** with intent invariant + `success_object: dual_offset_cells` + Prefer **concept** ok |
| Next | [[alpha0_stalberg_dual_visual_r3]] | dual_visual on the **correct** dual graph (after F5) |

## Intent invariant (exact)

`Player edits logic points; dual cells are the half-offset quads whose corners are those points.`

## Success object

`success_object: dual_offset_cells`

## Agree rationale

r1 Prefer-ok'd lattice **symbols** (`OrganicDualOffsetLattice`, `OwnedDualCellKeys`, `primary_face_as_dual` refuse) under staging Prefer without the § C.2 conceptual leg. Prefer/weave `prefer_intent_validates_gates` now requires concept Prefer (object identity + invariant) before dual/authorship chain-advance. This ticket re-arms the product altitude with that leg and refuses staging-only advance.

## Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Prefer **concept** ok (not staging Prefer alone): object identity + invariant; F5/MCP: click interior logic point → cyan on ≤4 `d_*` dual tiles (half-step), identical on repeat; not primary-face 2×2; organic + craft authority + rings=2 spacing=3.0 intact. |
| Out of scope | MeshLibrary dual_visual art polish, density lift, Terrain3D, Hex19 Success, chain-advance without concept Prefer |

## Refuse

- `proxy_substitution` · `intent_collapsed_to_mechanics`
- `primary_face_as_dual` · `stamp_as_dual` · `unstable_dual_neighborhood` · `over_neighbor_paint` · `skip_dual_offset`
- `points_as_grid` · `count_equals_topology` · `explicit_met_implicit_miss`
- `hex19_pick_as_craft_authority` · `gray_ramp_only` · `inspiration_shape_miss` · `terrain3d_in_scope` · `craft_cam_recenter_on_place`

## Prior altitude

| Slice | Disposition |
|-------|-------------|
| [[alpha0_stalberg_dual_neighborhood_r1]] | **partial_wrong_object** — stable ≤4 primary-face neighborhood |
| [[alpha0_stalberg_dual_lattice_r1]] | **superseded / partial_wrong_object** — lattice weld + staging Prefer; missing concept Prefer / conceptual leg |
| dual_visual r2/r3 | paused until dual lattice **concept** green + operator F5 |

## Kickoff

1. Harness proof (gate): r1-shaped primary-face host Prefer-fails; lattice+invariant host Prefer-passes — done before LIVE.
2. Write + prime r2 brief/armed; hub `armed_slice_id` → r2; greenlit true.
3. Slice Producer compose with conceptual leg (judgment — no structural-only Success).
4. IMPLEMENT_SLICE weld LIVE; Prefer **concept** ok; MCP a/b cyan on `d_*`.
5. Trinity push project tip (+ Prefer if needed). Receipt staging until operator F5. No Curator.

## Related

- Prefer/weave [[prefer_intent_validates_gates_r1]] · [[prefer_dual_object_identity_r1]] · [[Prefer-Authorship-Host-Law]] § C.2 / C.0b
- Series [[alpha0_stalberg_grid_kernel_r1]] · Next [[alpha0_stalberg_dual_visual_r3]]
