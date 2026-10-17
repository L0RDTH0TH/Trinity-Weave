---
slice_id: alpha0_stalberg_dual_rebind_r1
ask_id: alpha0_stalberg_dual_rebind
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2g
created: 2026-10-03
updated: 2026-10-04
operator_kill_at: 2026-10-04T03:13:23Z
superseded_reason: geometry_rethink_face_centroid_dual_verts
claim_class: aborted
factory_greenlit: false
status: aborted_superseded_by_geometry_rethink
prior_slice_id: alpha0_stalberg_primal_graph_r1
logic_prior_slice_id: alpha0_stalberg_primal_graph_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_primal_graph_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_rebind_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
success_object: dual_offset_cells
intent_invariant: "Player edits logic points; dual cells are the half-offset quads whose corners are those shared Vertex refs — cardinal (N/E/S/W) around the point, never a primary-face 2×2 block."
prefer_concept_required: true
---

# ⛔ OPERATOR KILL — ABORTED

**2026-10-04T03:13:23Z** — GREENLIGHT WELD stopped. No Success claim. Superseded by geometry rethink (dual vertices = primal face centroids / oskar Stage 6). See [[alpha0_stalberg_dual_geometry_rethink_investigation]].



# Slice brief — `alpha0_stalberg_dual_rebind_r1`

**GREENLIT** `2026-10-04T02:34:56Z` — dual ownership on MeshGraph incidence (neighbor placement fix). Operator F5 after [[alpha0_stalberg_primal_graph_r1]]: MeshGraph landed, **neighbor cluster still wrong**. **F5 clarification:** neighbors must be **cardinal** (N/E/S/W around the logic point) — **not** a filled 2×2 primary-face plate block. Prefer **concept** required. claim_class staging until operator F5.

## Project end-state (craft-plane north star)

Authorable irregular dual-grid craft plane on an organic all-quad board. Player edits **logic points**; dual cells are vertex-centered half-offset quads whose corners are **edge-neighbor MeshGraph Vertex refs**. Cyan / update-four = the **cardinal** dual tiles around the clicked point — never an axis-aligned 2×2 of primary faces/plates.

## Path position

| Leg | Slice | Role |
|-----|-------|------|
| Prior | [[alpha0_stalberg_primal_graph_r1]] | MeshGraph + incidence landed; F5 neighbor cluster still wrong |
| **This** | `alpha0_stalberg_dual_rebind_r1` | Cardinal dual ownership (edge-neighbor duals); kill face-block 2×2 |
| Next | [[alpha0_stalberg_dual_visual_r3]] | Dual visual on correct dual graph (after this F5) |

## Intent invariant (exact)

`Player edits logic points; dual cells are the half-offset quads whose corners are those shared Vertex refs — cardinal (N/E/S/W) around the point, never a primary-face 2×2 block.`

## Success object

`success_object: dual_offset_cells`

Corners MUST be MeshGraph Vertex singletons. Dual tile centred on a logic Vertex; corners = its edge-neighbors. Refuse `primary_face_as_dual` / `face_block_neighborhood`.

## Agree rationale

primal_graph_r1 Prefer-concept'd `organic_mesh_graph`, but dual ownership still selected **face-incident** duals (Varignon-in-face) — cyan reads as a filled **2×2 primary-face block**. Operator F5 clarification: Townscaper update-four must be the **cardinal** dual cells around the logic point (N/E/S/W), not that face plate block. This ticket rebinds dual cells to **vertex-centered** tiles (corners = edge-neighbor Vertex refs) so `DualCellsTouching(P)` = duals of P's edge-neighbors.

## Acceptance

| Field | Value |
|-------|--------|
| `done_when` | Prefer **concept** ok: `dual_offset_cells` + cardinal invariant; LIVE `DualCellsTouching` / `OwnedDualCellKeys` / `UpdateFour*` yield cardinal dual set around the logic Vertex (not face 2×2); cyan = those duals only; identical on repeat click; MeshGraph Vertex-ref corners; rings=2 spacing=3.0 + organic underlay intact. |
| Out of scope | MeshLibrary dual_visual art polish, density lift, Terrain3D, Hex19 Success, chain-advance without concept Prefer |

## Refuse

- `proxy_substitution` · `intent_collapsed_to_mechanics`
- `primary_face_as_dual` · `face_block_neighborhood` · `face_proxy_dual` · `support_face_index_as_dual_success`
- `face_scan_proxy_neighborhood` · `soft_take_4` · `valence_drop_editable`
- `unstable_dual_neighborhood` · `over_neighbor_paint` · `stamp_as_dual` · `skip_dual_offset`
- `indexed_lists_as_graph` · `ephemeral_edge_key_as_topology` · `non_unique_vertices`
- `points_as_grid` · `count_equals_topology` · `explicit_met_implicit_miss`
- `hex19_pick_as_craft_authority` · `gray_ramp_only` · `inspiration_shape_miss` · `terrain3d_in_scope` · `craft_cam_recenter_on_place`

## Kickoff

1. Write + prime brief/armed; hub `armed_slice_id` → dual_rebind_r1; greenlit true.
2. Slice Producer compose with full conceptual leg (judgment — structural-only / harness_fallback must fail).
3. IMPLEMENT_SLICE weld LIVE incidence-only dual ownership + valence residue fix.
4. Prefer **concept** ok; MCP repeat-click evidence.
5. Trinity push project tip (+ Prefer if scanners changed). Dual report A (outcome) + B (intent-seat). Receipt staging until operator F5. No Curator.

## Related

- Prefer/weave [[prefer_intent_validates_gates_r1]] · [[Prefer-Authorship-Host-Law]] § C.2
- Prior [[alpha0_stalberg_primal_graph_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]] · Next [[alpha0_stalberg_dual_visual_r3]]
