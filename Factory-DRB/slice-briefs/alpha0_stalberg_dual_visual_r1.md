---
slice_id: alpha0_stalberg_dual_visual_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2b
created: 2026-10-03
updated: 2026-10-03
greenlit_at: 2026-10-03T19:03:07Z
composed_at: 2026-10-03T18:50:52Z
claim_class: failed_altitude
factory_greenlit: false
status: failed_altitude_partial_visual_fidelity
altitude_note: Prefer ok then stretch-as-shape; see Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
superseded_by: alpha0_stalberg_dual_visual_r2
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_manual_scale_r1
logic_prior_slice_id: alpha0_stalberg_dual_corner_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
depends_on: alpha0_stalberg_dual_corner_r1
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_visual_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/Final-grid-state.jpg
trinity_branch: project/genesis-mythos-master
trinity_sha: 5c992107584340d3344dea7aa5e03e252bb7ad94
manual_limit: hex19_seed_rings_2
manual_spacing: 3.0
---

# Slice brief — `alpha0_stalberg_dual_visual_r1`

**GREENLIT** `2026-10-03T19:03:07Z` — `armed_ready_to_stage`. Weld in progress. `claim_class: staging` until operator F5.

Close the MeshLibrary / dual-visual fidelity gap left after [[alpha0_stalberg_dual_corner_r1]] logic Prefer: corner-config must select **shape-distinct** dual mesh variants (empty / edge / corner / full + rotation/mirror), not a gray albedo ramp on one quad plate. Keep organic craft-plane authority, dual-corner four-cell rebuild, and manual scale (rings=2, spacing=3.0).

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Topology: [[Grid-Topology-Host-Law]]. Prefer: [[Prefer-Authorship-Host-Law]].

## Why (serves primary craft-plane goal)

Primary goal = stable irregular all-quad lattice players/DMs author on (occupancy, dual-grid composition, later height/biome + intentional re-gen), compatible with dual-perspective VTT + open modular architecture.

- Kernel foundation + craft-plane authority + dual-corner **logic** exist at manual scale.
- Operator F5: yellow wire + blue → click light gray → neighbors darken = adjacency live, but visual is **gray ramp only**.
- LIVE: `DualGridCraftHost.Library => null`; `DualFamilyColor` gray ramp; `MeshLibrarySource = stalberg_organic_all_quad_graybox`.
- **Do not** treat dual_corner as product `ask_success`. Next Prefer = **dual visual / MeshLibrary fidelity**.

### Ticket-spec gap (why gray ramp shipped)

[[alpha0_stalberg_dual_corner_r1]] `done_when` said **“graybox OK”** without requiring:

1. corner-config → distinct mesh variant selection, or
2. Blender → MeshLibrary (or approved shape-distinct graybox stand-ins).

Townscaper grammar already requires corner-driven variant selection (“not one cube for every cell”); the dual_corner brief under-specified visual Success, so Prefer edges+faces could pass while F5 still looked like a brightness ramp.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_visual_r1` |
| Scope | Corner-config → MeshLibrary (or shape-distinct graybox) dual variants; refuse gray ramp; preserve organic + dual logic + manual scale |
| `claim_class` | `staging` until operator F5 |
| `factory_greenlit` | **`true`** (GREENLIGHT WELD) |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Mode | bind_dual_visual_meshlibrary_fidelity |

## 2. Acceptance (when greenlit)

| Field | Value |
|-------|--------|
| `done_when` | F5: flipping a logic corner rebuilds up to four dual cells with **shape-distinct** variants (empty/edge/corner/full + rot/mirror as appropriate) from corner config — readable without relying on albedo darkness; Prefer still `has_edges` + `has_faces_or_cells`; organic underlay + craft-plane authority + dual-corner logic preserved; rings=2 / spacing=3.0 knobs stay; regenerable |
| Pipeline | Explicit **Blender → MeshLibrary** **or** approved **shape-distinct graybox stand-ins** (geometry differs per family — not `DualFamilyColor` ramp on one plate) |
| Out | density lift · Terrain3D · art-bind polish · cam yank · Hex19 tutorial Success · full Phase-2 POIs · dual_corner product ask_success by this draft alone |

## 3. Refuse

**New:** `gray_ramp_only` — claiming dual visual Success when cells differ only by gray albedo / alpha on the same plate mesh (LIVE `DualFamilyColor` pattern).

**Keep:** `inspiration_shape_miss`, `skip_dual_offset`, `prop_scatter_as_composition`, `bitmask_equals_townscaper`, `points_as_grid`, `count_equals_topology`, `hex_scaffold_as_final_mesh`, `hex19_pick_as_craft_authority`, `dual_overlay_as_grid_kernel`, kernel refuses (`non_unique_vertices`, `naive_laplacian_only`, `missing_square_area_force`, `free_boundary_fold`, `extrusion_before_2d_stable`, `noodle_edge_clutter`, …), `terrain3d_in_scope`, `craft_cam_recenter_on_place`, `verify_mcp_only`.

## 4. Preserved priors (must not regress)

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_topology_base_r1]] | Organic all-quad injective topo underlay |
| [[alpha0_stalberg_craft_plane_authority_r1]] | Pick/paint / `ICraftCellAuthority` on OrganicQuadMesh |
| [[alpha0_stalberg_dual_corner_r1]] | Logic points + four dual cells rebuild on flip (**logic** preserved; visual upgraded here) |
| [[alpha0_stalberg_manual_scale_r1]] | `DefaultRingCount=2`, `DefaultSpacing=3.0`; density lift deferred |

Prefer edges+faces remain green. `claim_class: staging` until operator F5 — no product `ask_success` from Prefer alone.

## 5. Load set (before code, after GREENLIGHT)

- [ ] [[FEEDSTOCK-SHAPE]]
- [ ] [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] — dual cells sample four corners → MeshLibrary entry + rot/mirror
- [ ] [[Grid-Topology-Host-Law]] · [[Prefer-Authorship-Host-Law]]
- [ ] [[COHESIVE-VISION-ART-DIRECTION]]
- [ ] Host-weld pilots: `implementation_factory_loop` + `product_factory_pipeline`
- [ ] Goal class: [[Ingest/Final-grid-state.jpg]] (board silhouette; dual variants are authorship grammar, not art polish)

## 6. Kickoff (operator)

1. Review this draft (+ Grok validate on Trinity orphan tip).
2. Say **GREENLIGHT WELD** in chat (no YAML latch).
3. Module lane only; Prefer + MCP aid; operator F5 closes staging.
4. **No Curator.** No LIVE weld until greenlit.

## Related

- Logic prior [[alpha0_stalberg_dual_corner_r1]] · Scale [[alpha0_stalberg_manual_scale_r1]] · Craft [[alpha0_stalberg_craft_plane_authority_r1]] · Foundation [[alpha0_stalberg_topology_base_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]
