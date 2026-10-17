---
slice_id: alpha0_stalberg_dual_neighborhood_r1
ask_id: alpha0_stalberg_dual_neighborhood
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2c
created: 2026-10-03
updated: 2026-10-03
claim_class: staging
wrong_object_altitude: primary_face_neighborhood_as_dual
superseded_by: alpha0_stalberg_dual_lattice_r1
factory_greenlit: true
status: partial_wrong_object_altitude
prior_slice_id: alpha0_stalberg_dual_visual_r2
logic_prior_slice_id: alpha0_stalberg_dual_corner_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_craft_plane_authority_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_neighborhood_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
validation_status: confirmed_2026-10-03
---

# Slice brief — `alpha0_stalberg_dual_neighborhood_r1` (draft)

**GREENLIT** `2026-10-03T20:37:43Z` — Prefer bind + IMPLEMENT_SLICE module lane. claim_class staging until operator F5.

Fix the dual-graph neighborhood before any further dual-visual variant work.

Operator F5 sequence (2026-10-03) proved:
- Same logic-point click produces **different** neighbor sets on repeat.
- Updates look like independent occupancy stamps, not “the four dual cells that share this logic point.”
- Dual-visual r1/r2 therefore cannot be evaluated — variant selection is premature while ownership is unstable.

## Validation evidence (LIVE — confirmed before drafting)

| Check | Result | Evidence |
|-------|--------|----------|
| Dual cells = shared logic corners? | **No — stamp_as_dual** | `PlaceDiscreteDualLibraryItem` places MeshLibrary items at face **centroid** + uniform scale (`DualGridCraftHost.cs`); MCP F5 shows `DualCell_org_N_<Family>` independent plates under `OrganicDualCornerOverlay` (50 slots). |
| Interior updates ≤4 via corner ownership? | **Partial / soft** | Corner path uses `_vertexToFaces` + `Take(MaxDualCellsPerLogicFlip)` but still refreshes after `over_neighbor_paint` warn (soft truncate, not hard refuse). Face paint path updates **one** dual + paints occupancy plate (`EnsureFilledOrganicFaceMesh`). |
| Same point → identical dual-cell set? | **Unstable in practice** | `TryPickOrganicCorner` nearest-within-`0.55*_hexSize` can resolve different vertices for “same” visual click; visible family of shared cells also changes with prior corner state (east then north). Debug labels exist (`RefreshDebugDualCellIds`) but ownership is not F5-legible as a stable four-cell set. |
| Grok smoking gun | **Confirmed** | Dual graph ownership not product-legible; boxes behave as independent stamps with state-dependent neighborhood appearance. |

MCP note: runtime `call_method` unavailable for C# FlipOrganicCorner in this session; confirmation is code + live overlay inspection (`DualSlotCount=50`, `PaintedCellCount=0`, seeded Corner/Edge/Full plates).

## Why

Townscaper dual-grid grammar (locked):
1. Logic points are the editable corners.
2. Each dual visual cell has four corners that are logic points.
3. Flipping one logic point rebuilds **exactly** the dual cells that reference it (≤4 interior; fewer on boundary).
4. That set is **geometric and stable** — identical every time for the same point.

Current LIVE fails (3). Dual-visual tickets assumed (3) was already true. It is not.

## Acceptance (when greenlit)

| Field | Value |
|-------|--------|
| `done_when` | For any interior logic point P: the set of dual cells that reference P is exactly four, identical on every repeated click of P, and only those cells update. Boundary points may have fewer. Debug highlight (distinct color, one frame or until next click) makes the set visible on F5. Organic underlay + craft-plane authority + manual scale (rings=2, spacing=3.0) preserved. |
| Out of scope | MeshLibrary art, empty/edge/corner/full silhouette polish, density lift, Terrain3D, Hex19 Success, dual_visual product ask_success |

## Refuse (new + carried)

**New:**
- `unstable_dual_neighborhood` — same logic point yields different dual-cell sets across clicks
- `over_neighbor_paint` — interior point updates more than four dual cells
- `stamp_as_dual` — independent occupancy stamps instead of dual cells owned by shared logic corners

**Keep:** `points_as_grid`, `count_equals_topology`, `hex19_pick_as_craft_authority`, `gray_ramp_only`, `inspiration_shape_miss`, `skip_dual_offset`, kernel refuses, `terrain3d_in_scope`, `craft_cam_recenter_on_place`

## Preserved priors

| Prior | Must not regress |
|-------|------------------|
| topology_base_r1 | Organic all-quad injective underlay |
| craft_plane_authority_r1 | Pick/paint on OrganicQuadMesh |
| manual_scale_r1 | rings=2, spacing=3.0 |
| dual_corner_r1 | Logic-point flip path exists (neighborhood corrected here) |

## Dual-visual pause

`alpha0_stalberg_dual_visual_r2` Prefer harden landed but **ask_success paused**. `next_in_chain`: [[alpha0_stalberg_dual_visual_r3]] only after this neighborhood Prefer is green on F5.

## Kickoff

1. Review + Grok validate.
2. Operator says **GREENLIGHT WELD**.
3. Module lane only; Prefer + MCP; operator F5 closes staging.
4. No Curator. LIVE weld authorized under greenlight.


## Partial / wrong-object altitude (2026-10-03)

Operator + Grok F5: cyan highlight was a **stable 2×2 of primary organic faces**, not dual-lattice cells around a logic point. Prefer ok on stability only. Superseded by [[alpha0_stalberg_dual_lattice_r1]] (`primary_face_as_dual` refuse).
