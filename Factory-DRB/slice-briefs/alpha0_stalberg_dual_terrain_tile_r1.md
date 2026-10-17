---
slice_id: alpha0_stalberg_dual_terrain_tile_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
umbrella_ask_id: alpha_architecture_half_b
series_step: 2o
created: 2026-10-04
updated: 2026-10-04
prefer_ok_at: '2026-10-04T21:17:52Z'
composed_at: '2026-10-04T21:14:21Z'
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_concept_required: true
status: greenlit_weld_live_staging_awaiting_f5
template: Half-B-Weld-Brief-Template
prior_slice_id: alpha0_stalberg_dual_mesh_fit_r1
supersedes_success:
  - alpha0_stalberg_dual_art_style_r1
keeps_geometry_from: alpha0_stalberg_dual_stage6_cell_r1
depends_on: alpha0_stalberg_dual_mesh_fit_r1
discrete_bind_cite: alpha0_stalberg_dual_visual_r3
armed_packet: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/alpha0_stalberg_dual_terrain_tile_r1.armed.yaml
topology_law: Grid-Topology-Host-Law
prefer_law: Prefer-Authorship-Host-Law
prefer_harden: prefer_dual_terrain_tile_authorship_r1
prefer_audit: Prefer-Audit-dual_visual_r1-stretch-pattern-2026-10-03
craft_grammar: Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI
goal_image: Ingest/nature-pack.png
gold_sixpack_evidence: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/_evidence/gold_dual_offset_terrain_tile_sixpack/
density_lift_live: rings_5_spacing_210
success_object: dual_offset_terrain_tile
contract: C_dual_offset_terrain_tile_land_water_read
camera_altitude: separate_live_craft_cam_tilt_not_prefer_success
grok_diagnosis: cream_blobs_wrong_success_object_on_art_style_r1
---

# Slice brief — `alpha0_stalberg_dual_terrain_tile_r1`

**Prefer concept / arm only** — **not** GREENLIGHT WELD LIVE. Cause of cream blobs = wrong Success named on [[alpha0_stalberg_dual_art_style_r1]] (Prefer scored what was written). Fix = re-object Prefer seat to **`dual_offset_terrain_tile`**.

Umbrella: [[alpha_architecture_half_b]]. Series: [[alpha0_stalberg_grid_kernel_r1]]. Prefer: [[Prefer-Authorship-Host-Law]] § C.1b. Harden: [[prefer_dual_terrain_tile_authorship_r1]]. Topology: [[Grid-Topology-Host-Law]]. Grammar: [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. Geometry KEEP: [[alpha0_stalberg_dual_mesh_fit_r1]] · [[alpha0_stalberg_dual_stage6_cell_r1]]. Discrete bind cite-only: [[alpha0_stalberg_dual_visual_r3]] (not terrain Success).

## Why (Grok + operator)

- [[alpha0_stalberg_dual_art_style_r1]] Prefer-ok'd **cream quarter-platforms** — metrics/GLB/AABB green; operator eye reads sage/cream **plinths**, not terrain.
- [[alpha0_stalberg_dual_visual_r3]] = discrete MeshLibrary bind only — **not** terrain ask_success.
- Dual cell **is** the terrain you see; organic cream underlay recedes; neighbors share one foundation language so a filled patch reads as **ground**.

## 1. Header

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_stalberg_dual_visual` |
| `slice_id` | `alpha0_stalberg_dual_terrain_tile_r1` |
| `success_object` | **`dual_offset_terrain_tile`** |
| Scope | Corner-config → discrete land/water tile readable from craft cam as terrain/ground (not plinth) |
| `claim_class` | `staging` until operator F5 after LIVE weld |
| `factory_greenlit` | **`false`** — LIVE weld blocked until gold sixpack + operator GREENLIGHT WELD LIVE |
| LIVE | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` (no replace this Prefer) |
| Mode | `dual_offset_terrain_tile_land_water_read` |

## 2. Focus inspirations (bind into done_when)

| Source | Why in focus |
|--------|----------------|
| [[Ingest/nature-pack.png]] / [[Ingest/nature-pack-arial.png]] | Mossy rock, sage hill, soft land/water bevel — readable from above |
| [[Ingest/Model-pack.png]] | Earth / sage / stone / water — thick toy mass, one family |
| Factory-DRB/references/craft-visual-r2/ | Same packs filed for craft-visual-r2 |
| Townscaper density (YT + stills) | Tiles **coalesce** into one craft layer — **not** Townscaper houses / sea-grid clone |
| Astroneer / [[Visual-Factory-Direction-Stylized-Low-Poly]] | Stylized low-poly bar |
| [[Ingest/Screenshot_20261004_003640_YouTube.jpg]] · YT stills | Prior dual-grid stills — density/grammar cite; cream quarters = **wrong Success exemplar** |
| Grok diagnosis (2026-10-04) | Cream blobs = wrong Success object / metrics-only altitude |

### Gold sixpack (required before LIVE GREENLIGHT)

Placeholder evidence dir: `_evidence/gold_dual_offset_terrain_tile_sixpack/` — **do not invent fake gold images**. Operator/Grok generates eye-test sixpack; Prefer cannot fake with another plinth drop.

## 3. Variant reads (must)

| Variant | Must read as |
|---------|----------------|
| Empty | Water / sand plate |
| Full | Mossy land mass |
| Edge | Shore (land \| water) |
| Corner | Convex land into water |
| InverseCorner | Concave cove |
| Diagonal | Two opposite corners filled |

**Place** = translate + yaw only. No stretch-as-shape. One click ≤4 duals. Mesh-fit warp to secondary corners = **placement KEEP**, not Success substitute.

## 4. Acceptance

| Field | Value |
|-------|--------|
| `done_when` | **F5 (only ask_success):** from craft cam, filled cluster reads as **terrain/ground**; name Empty vs Full vs Corner without debug overlay; cream underlay not the read; six variants match land/water table; mesh_fit/Stage-6/secondary glow/squarify/rings=5 spacing=210 KEEP; Prefer refuses plinth/blob/metrics-only/stretch/gray_ramp/prop_scatter/inspiration_shape_miss/procedural_only/proxy_substitution |
| Out | GREENLIGHT WELD LIVE this Prefer · cream/sage plinth Success · dual_visual_r3 / art_style_r1 ask_success · Terrain3D · density-beyond-5 · cam tilt as Prefer Success · inventing gold images |

## 5. Refuse (`do_not_waive`)

| Code | Kills |
|------|--------|
| `plinth_as_terrain` | Single rounded block / low-vert Full / one material as land |
| `blob_as_module` | Organic cream is the readable surface |
| `metrics_only_glb_drop` | File exists / MeshLibrary id / AABB as Success |
| `gray_ramp_only` / `stretch_as_variant` | Carry from dual-visual C.1 |
| `prop_scatter_as_composition` | Toys that don't coalesce into mass |
| `inspiration_shape_miss` | Widened: nameable variants vs nature+model pack gold |
| `procedural_only_as_success` | Blender primitives don't get a pass |
| `verify_mcp_only` / `proxy_substitution` / `intent_collapsed_to_mechanics` | Metrics / mechanical Prefer ≠ intent |

Plus prior dual refuses: `primary_face_as_dual` · `over_neighbor_paint` · `skip_dual_offset` · `terrain3d_in_scope` · `cam_tilt_as_art_prefer_success`.

## 6. Preserved priors

| Prior | Requirement |
|-------|-------------|
| [[alpha0_stalberg_dual_mesh_fit_r1]] | Bilinear warp KEEP (placement) |
| [[alpha0_stalberg_dual_visual_r3]] | Discrete family ids cite — **not** terrain Success |
| [[alpha0_stalberg_dual_stage6_cell_r1]] | Stage-6 dual wire KEEP |
| [[alpha0_stalberg_dual_secondary_glow_center_r1]] | Secondary glow/pick KEEP |
| [[alpha0_stalberg_quad_kernel_squarify_r1]] | Stage-5 squarify KEEP |
| Density lift LIVE | rings=5 · spacing=210 |
| Cam | CraftPlanarCamRig pitch — separate LIVE, not Prefer Success |

## 7. Operator next (binding)

1. **Gold sixpack eye-test** into `_evidence/gold_dual_offset_terrain_tile_sixpack/` (Grok/operator).
2. Then operator **GREENLIGHT WELD LIVE** (separate kickoff) — replace cream/sage plinth MeshLibrary with terrain tiles.
3. F5 ask_success only on terrain read bar. Ban MCP-only attest.
4. Prefer/weave harden [[prefer_dual_terrain_tile_authorship_r1]] keeps cream-style Success Prefer-failing.

## Related

- Supersedes Success: [[alpha0_stalberg_dual_art_style_r1]] · Discrete bind: [[alpha0_stalberg_dual_visual_r3]] · Harden: [[prefer_dual_terrain_tile_authorship_r1]] · Series: [[alpha0_stalberg_grid_kernel_r1]]
