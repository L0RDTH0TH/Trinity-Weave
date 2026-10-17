---
slice_id: alpha0_stalberg_dual_secondary_glow_center_r1
ask_id: alpha0_stalberg_dual_secondary_glow_center
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2k
created: 2026-10-04
updated: 2026-10-04
greenlit_at: 2026-10-04T07:08:00Z
claim_class: staging
factory_greenlit: true
status: armed_ready_to_stage
prior_slice_id: alpha0_stalberg_dual_glow_neighborhood_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
logic_prior_slice_id: alpha0_stalberg_primal_graph_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_dual_glow_neighborhood_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_secondary_glow_center_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
annotate_proof: Ingest/Screenshot from 2026-10-04 01-19-00.png
bug_image: Ingest/Screenshot from 2026-10-04 01-19-00.png
goal_image_note: secondary-first glow cluster centered on coral/cyan dual verts; Stage-6 wire kept
terminology: Untitled.md Final-Grid dual vocabulary table
trinity_branch: project/genesis-mythos-master
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
success_object: dual_offset_cells
intent_invariant: "Stage-6 DualCell identity (OwnedDualCellKeys=one; dual verts=face centroids; dual edges centroid–centroid) remains lattice wire/topology; pick/glow/populate centers on the secondary grid — nearest face-centroid dual vert — via SmallCornerQuadsAroundFace(F) (typically 4 pie sectors meeting at the coral/cyan secondary locus); SmallCornerQuadsAround(V) primary-star is not Prefer Success; Stage-6 wire kept; refuse primary_star_glow_as_success / primary_face_as_dual / stage6_union_as_single_glow_tile."
prefer_concept_required: true
investigation: alpha0_stalberg_dual_geometry_rethink_investigation
contract: C_secondary_glow_center_keep_stage6_wire_small_corner_units
---

# Slice brief — `alpha0_stalberg_dual_secondary_glow_center_r1`

**GREENLIT** `2026-10-04T07:08:00Z` — center glow (and pick/snap for craft populate) on the **secondary** dual locus. Keeps Stage-6 wire + small-corner-quad units from [[alpha0_stalberg_dual_glow_neighborhood_r1]] / [[alpha0_stalberg_dual_stage6_cell_r1]]. Prefer **concept** required. claim_class staging until operator F5. **No MeshLibrary models** this Prefer.

## Bug / misunderstanding (operator scrap)

Prior Prefer (`dual_glow_neighborhood_r1`) correctly made glow units = small corner quads, but pick/glow still **starred from amber primary V** (`TryPickOrganicCorner` → `SmallCornerQuadsAround(V)`). Operator intent simplified: center the glow on the **secondary** (dual verts at face centroids / coral spheres / cyan lattice points) so the cluster reads secondary-first — then move to models.

| Current LIVE (wrong for this ask) | Success |
|-----------------------------------|---------|
| Pick nearest **primary** V | Pick nearest **secondary** point (face centroid) |
| Glow = `SmallCornerQuadsAround(V)` starring from amber | Glow = `SmallCornerQuadsAroundFace(F)` meeting at coral/cyan |
| Visual center locked to orange vertex | Visual center = secondary locus |

## Contract (C)

1. **Pick:** nearest editable secondary face centroid (dual vert).
2. **Glow set:** small corner quads **incident to** that secondary point (typically 4 around a quad face).
3. **Keep:** Stage-6 dual wire (centroid–centroid crossing amber); small-corner-quad populate units; craft cam 7× / zoom / DualLatticeDebug spheres.
4. **Do not** revert to FaceCornersLocal / primary_face_as_dual / fill whole main cell / Stage-6 union as single glow tile.
5. **Refuse** `primary_star_glow_as_success` when Prefer claims secondary-centered.

## Path position

| Leg | Slice | Role |
|-----|-------|------|
| Prior geometry | [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 wire KEEP |
| Prior glow units | [[alpha0_stalberg_dual_glow_neighborhood_r1]] | SmallCornerQuad unit KEEP |
| **This** | `alpha0_stalberg_dual_secondary_glow_center_r1` | Pick/glow center → secondary |
| Next | [[alpha0_stalberg_dual_visual_r3]] | MeshLibrary / models (after this F5) |

## Intent invariant (exact)

`Stage-6 DualCell identity (OwnedDualCellKeys=one; dual verts=face centroids; dual edges centroid–centroid) remains lattice wire/topology; pick/glow/populate centers on the secondary grid — nearest face-centroid dual vert — via SmallCornerQuadsAroundFace(F) (typically 4 pie sectors meeting at the coral/cyan secondary locus); SmallCornerQuadsAround(V) primary-star is not Prefer Success; Stage-6 wire kept; refuse primary_star_glow_as_success / primary_face_as_dual / stage6_union_as_single_glow_tile.`

## Success object

`success_object: dual_offset_cells` with secondary-centered glow/pick (Prefer text / structural Success — intent validates gates).

## Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Prefer **concept** ok: pick snaps to secondary face centroid; glow cluster visual center is that locus (`SmallCornerQuadsAroundFace`); Stage-6 wire + small-corner units kept; cyan crosses amber; DualLatticeDebug spheres intact; refuse `primary_star_glow_as_success`. |
| Out of scope | MeshLibrary dual_visual art, density lift, Terrain3D, Hex19 Success, chain-advance without concept Prefer |

### F5 attest

1. Open `res://scenes/WorldgenCraft.tscn`, F5 / play.
2. Click near a **coral sphere / cyan lattice** secondary point → glow centers there (pie sectors around that point).
3. Confirm glow is **not** a 2×2 (or N) star locked to an amber primary vertex.
4. Cyan still crosses amber; spheres at face centres; HUD `SEC-GLOW r1`.
5. Craft cam 7× / zoom / DualLatticeDebug spheres still work.

## Refuse

- `primary_star_glow_as_success` · `proxy_substitution` · `intent_collapsed_to_mechanics`
- `stage6_union_as_single_glow_tile` · `owned_only_glow` · `primary_face_as_dual`
- `inset_face_corners_as_dual` · `face_corners_local_as_dual_edges` · `face_block_neighborhood`
- `hex19_always_4` · `soft_take_4` · `vertex_neighbor_as_dual_corner`
- `dual_rebind_cardinal_wrong_locus` · `gray_ramp_only` · `inspiration_shape_miss`
- `terrain3d_in_scope` · `craft_cam_recenter_on_place` · `verify_mcp_only`

## Kickoff

1. Write + prime brief/armed; hub `armed_slice_id` → secondary_glow_center_r1; greenlit true.
2. Slice Producer compose with full conceptual leg.
3. IMPLEMENT_SLICE: `TryPickOrganicSecondary` + `SmallCornerQuadsAroundFace` highlight/UpdateFour; Stage-6 wire kept.
4. Prefer **concept** ok; MCP / F5 evidence.
5. Trinity push when path allows; note cooldown. Curator snapshot `"dual secondary glow center r1"`.

## Related

- Prior [[alpha0_stalberg_dual_glow_neighborhood_r1]] · Geometry [[alpha0_stalberg_dual_stage6_cell_r1]]
- Annotate [[Ingest/Screenshot from 2026-10-04 01-19-00.png]] · Goal [[Ingest/Final-grid-state.jpg]] · Terminology [[Untitled]]
- Prefer/weave [[prefer_intent_validates_gates_r1]] · [[Prefer-Authorship-Host-Law]] § C.2
- Series [[alpha0_stalberg_grid_kernel_r1]] · Next [[alpha0_stalberg_dual_visual_r3]]
