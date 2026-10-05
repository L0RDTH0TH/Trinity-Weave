---
slice_id: alpha0_stalberg_dual_glow_neighborhood_r1
ask_id: alpha0_stalberg_dual_glow_neighborhood
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2j
created: 2026-10-04
updated: 2026-10-04
revised_at: 2026-10-04T06:44:02Z
revise_note: operator_clarify_small_corner_quads_not_stage6_union_glow
greenlit_at: 2026-10-04T06:37:05Z
claim_class: staging
factory_greenlit: true
status: armed_ready_to_stage
prior_slice_id: alpha0_stalberg_dual_stage6_cell_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
logic_prior_slice_id: alpha0_stalberg_primal_graph_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_dual_stage6_cell_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_glow_neighborhood_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
annotate_proof: Ingest/Screenshot from 2026-10-04 01-19-00.png
bug_image: Ingest/Screenshot from 2026-10-04 01-19-00.png
goal_image_note: graph-family compare — glow cardinality 2 edge / 4 interior; cyan still crosses amber
terminology: Untitled.md Final-Grid dual vocabulary table
trinity_branch: project/genesis-mythos-master
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
success_object: dual_offset_cells
intent_invariant: "Player edits logic points (primal Vertices); Stage-6 DualCell identity (OwnedDualCellKeys=one; dual verts=face centroids; dual edges centroid–centroid) remains lattice wire/topology; pick/glow/populate uses SmallCornerQuadsAround(V) — the degree-many primary-edge-carved corner sectors (typically 2 edge / 4 interior), each with corners V, mid(incident edge), faceCentroid(F), mid(other incident edge); Stage-6 polygon is the union of those pieces and must not be a single glow/fill tile; refuse primary_face_as_dual / stage6_union_as_single_glow_tile."
prefer_concept_required: true
investigation: alpha0_stalberg_dual_geometry_rethink_investigation
contract: B_small_corner_quads_glow_keep_stage6_wire
---

# Slice brief — `alpha0_stalberg_dual_glow_neighborhood_r1`

**GREENLIT** `2026-10-04T06:37:05Z` — dual **glow / update-neighborhood** cardinality fix on Stage-6 identity. Keeps [[alpha0_stalberg_dual_stage6_cell_r1]] geometry (DualCell = Stage-6 polygon around logic V; dual verts = face centroids; cyan crosses amber). Prefer **concept** required. claim_class staging until operator F5.

## Bug proof (operator annotate + drift)

Cite [[Ingest/Screenshot from 2026-10-04 01-19-00.png]] (annotated after Stage-6 cell F5):

| Pick | Annotate intent | LIVE failure (stage6_cell_r1) |
|------|-----------------|-------------------------------|
| Edge-ish (Red) | **2** dual cells glow; **2** far main verts via those quads | `OwnedDualCellKeys(V)=1` → `HighlightOwnedDualCells` shows **1** |
| Interior (Purple) | **4** dual cells glow; **4** far main verts | same always-1 owned-only highlight |
| Shared | Red/Purple may share an expansion main vert | OK if ownership stays 1:1 DualCell↔owner |

Root cause: geometry identity improved, but **glow/update set collapsed to owned-only**. Annotate counts the **expand neighbour DualCells** (degree-dependent), not the single owned Stage-6 cell around V, and not `1+degree`.

## Contract (B) — revised (operator clarify)

Keep Stage-6 **wire/topology** (dual verts at face centroids; cyan crosses amber). Glow/populate unit = **small_corner_quads**:

1. **OwnedDualCellKeys(V)** may stay one Stage-6 cell for lattice topology (≥3 faces) — **not** the glow fill object.
2. **SmallCornerQuadsAround(V)** = one primary-edge-carved corner sector per incident Face F — typically **2** edge / **4** interior.
3. Each small quad corners: **V**, **mid(edge V→next)**, **faceCentroid(F)**, **mid(edge prev→V)** (Varignon / Townscaper corner sector). Primary edges form two sides.
4. Stage-6 polygon around V = **union** of those pieces — refuse `stage6_union_as_single_glow_tile`.
5. Highlight / UpdateFour / populate use the N small quads — never fill whole main cell (`primary_face_as_dual`).

## Project end-state (craft-plane north star)

Authorable irregular dual-grid craft plane. Stage-6 polarity preserved; pick feedback shows the **secondary expand neighborhood** that Townscaper-style update touches — not a single owned tile sold as the whole glow story.

## Path position

| Leg | Slice | Role |
|-----|-------|------|
| Prior geometry | [[alpha0_stalberg_dual_stage6_cell_r1]] | DualCell = Stage-6; cyan crosses amber — **KEEP** |
| **This** | `alpha0_stalberg_dual_glow_neighborhood_r1` | Glow/update set = ExpandDualNeighborKeys (2/4) |
| Next | [[alpha0_stalberg_dual_visual_r3]] | Dual visual on correct dual graph (after this F5) |

## Intent invariant (exact)

`Player edits logic points (primal Vertices); DualCell identity remains the Stage-6 polygon of face centroids around V (OwnedDualCellKeys=one); on pick/flip of V the highlight and UpdateFour expand set is the degree-dependent dual-edge neighbour DualCells (ExpandDualNeighborKeys) — typically 2 at edge-ish sites and 4 at interior — matching annotate; dual verts stay at face centres; dual edges stay centroid–centroid; shared expansion main verts OK without dual-owning one DualCell.`

## Success object

`success_object: dual_offset_cells` with Stage-6 identity **plus** expand-glow cardinality matching annotate (Prefer text / structural Success — intent validates gates).

## Agree rationale

stage6_cell_r1 Prefer-concept'd DualCell = Stage-6 around V and fixed cyan/amber crossing, but highlight stayed `OwnedDualCellKeys`-only (`MaxOwned=1`). Annotate + drift investigation require degree-dependent secondary expand set (2 edge / 4 interior), not owned-only and not Hex19 soft-pad always-4.

## Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Prefer **concept** ok: `dual_offset_cells` + Stage-6 identity preserved + ExpandDualNeighborKeys glow/update cardinality matches annotate (edge≈2, interior≈4); OwnedDualCellKeys(V)=one; cyan still crosses amber; spheres at face centres; dual≈Stage-6 count; shared expansion vert OK; no FaceCornersLocal / primary_face_as_dual / revert; craft cam 7× / zoom / DualLatticeDebug spheres intact. |
| Out of scope | MeshLibrary dual_visual art polish, density lift, Terrain3D, Hex19 Success, chain-advance without concept Prefer |

### F5 attest

1. Click edge-like Red-analogue → **2** dual cells glow.
2. Click interior Purple-analogue → **4** dual cells glow.
3. Cyan still crosses amber; spheres at face centres; dual≈ Stage-6 count.
4. Shared expansion vert possible between two picks without one DualCell having two owners.

## Refuse

- `proxy_substitution` · `intent_collapsed_to_mechanics`
- `stage6_union_as_single_glow_tile` · `owned_only_glow` · `glow_owned_only_when_expand_intent` · `max_owned_1_as_glow_success`
- `hex19_always_4` · `soft_take_4` · `soft_pad_expand_to_4`
- `primary_face_as_dual` · `inset_face_corners_as_dual` · `face_corners_local_as_dual_edges`
- `vertex_neighbor_as_dual_corner` · treating CornerVertices as dual corners
- `dual_rebind_cardinal_wrong_locus` · reverting Stage-6 DualCell identity to face-as-dual
- `face_block_neighborhood` · `over_neighbor_paint` · `unstable_dual_neighborhood`
- `stamp_as_dual` · `skip_dual_offset` · `valence_drop_editable`
- `hex19_pick_as_craft_authority` · `gray_ramp_only` · `inspiration_shape_miss` · `terrain3d_in_scope` · `craft_cam_recenter_on_place`

## Kickoff

1. Write + prime brief/armed; hub `armed_slice_id` → dual_glow_neighborhood_r1; greenlit true; keep stage6 geometry.
2. Slice Producer compose with full conceptual leg (judgment — structural-only / harness_fallback must fail).
3. IMPLEMENT_SLICE: `SmallCornerQuadsAround` + highlight/UpdateFour on small quads; Stage-6 wire kept; HUD GLOW-NBR.
4. Prefer **concept** ok; MCP / F5 evidence (2/4 glow; cyan crosses amber).
5. Trinity push project tip when Prefer path established. Dual report A + B. Receipt staging until operator F5. Curator snapshot `"dual glow neighborhood r1 weld"`.

## Related

- Annotate [[Ingest/Screenshot from 2026-10-04 01-19-00.png]] · Goal [[Ingest/Final-grid-state.jpg]] · Terminology [[Untitled]]
- Keeps geometry [[alpha0_stalberg_dual_stage6_cell_r1]] · Investigation [[alpha0_stalberg_dual_geometry_rethink_investigation]]
- Prefer/weave [[prefer_intent_validates_gates_r1]] · [[Prefer-Authorship-Host-Law]] § C.2
- Series [[alpha0_stalberg_grid_kernel_r1]] · Next [[alpha0_stalberg_dual_visual_r3]]
